from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
import pymysql
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL - MySQL configuration
DEFAULT_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/real_estate_db"
DATABASE_URL = config("DATABASE_URL", default=DEFAULT_DATABASE_URL)

# Managed providers hand out plain mysql:// URLs, which SQLAlchemy would resolve to the unavailable
# MySQLdb driver. Always use PyMySQL.
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = "mysql+pymysql://" + DATABASE_URL[len("mysql://"):]

# DigitalOcean (and most managed MySQL) require TLS and append "?ssl-mode=REQUIRED", which PyMySQL does
# not understand. Translate it into PyMySQL's ssl option. Set DATABASE_SSL_CA to a CA certificate file
# to also verify the server certificate; otherwise the connection is encrypted but not verified.
_url = make_url(DATABASE_URL)
_ssl_mode = str(_url.query.get("ssl-mode", _url.query.get("ssl_mode", ""))).upper()
_use_ssl = _ssl_mode in {"REQUIRED", "VERIFY_CA", "VERIFY_IDENTITY"} or config("DATABASE_SSL", default=False, cast=bool)
if "ssl-mode" in _url.query or "ssl_mode" in _url.query:
    DATABASE_URL = _url.difference_update_query(["ssl-mode", "ssl_mode"]).render_as_string(hide_password=False)

_ssl_ca = config("DATABASE_SSL_CA", default="")
CONNECT_ARGS = {}
if _use_ssl:
    CONNECT_ARGS["ssl"] = {"ca": _ssl_ca} if _ssl_ca else {"check_hostname": False}

if DATABASE_URL == DEFAULT_DATABASE_URL:
    logger.warning("Using default database configuration. Set DATABASE_URL in the environment.")


def create_database_if_not_exists():
    """Create the database if it doesn't exist (best effort; managed DBs usually already have one)."""
    try:
        url = make_url(DATABASE_URL)
        if not url.database:
            return False
        connection = pymysql.connect(
            host=url.host or "localhost",
            port=url.port or 3306,
            user=url.username,
            password=url.password or "",
            charset="utf8mb4",
            ssl=CONNECT_ARGS.get("ssl"),
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{url.database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.close()
        return True
    except Exception as e:
        logger.warning(f"Could not auto-create database (continuing): {e}")
        return False


# Create database if it doesn't exist
create_database_if_not_exists()

engine = create_engine(
    DATABASE_URL,
    connect_args=CONNECT_ARGS,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=config("DB_ECHO", default=False, cast=bool)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
