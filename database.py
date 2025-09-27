from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
import pymysql
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL - MySQL configuration
DATABASE_URL = config(
    "DATABASE_URL", 
    default="mysql+pymysql://root:password@localhost:3306/real_estate_db"
)

# Check if using default configuration
if DATABASE_URL == "mysql+pymysql://root:password@localhost:3306/real_estate_db":
    logger.warning("Using default database configuration. Consider creating a .env file with your actual database settings.")
    logger.info("Default config: mysql+pymysql://root:password@localhost:3306/real_estate_db")

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    try:
        # Parse the database URL to get connection details
        url_parts = DATABASE_URL.split('://')[1].split('@')
        auth_part = url_parts[0].split(':')
        host_port_part = url_parts[1].split('/')
        
        username = auth_part[0]
        password = auth_part[1] if len(auth_part) > 1 else ''
        host_port = host_port_part[0].split(':')
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 3306
        database = host_port_part[1] if len(host_port_part) > 1 else 'real_estate_db'
        
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"Database '{database}' created or already exists")
        
        connection.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

# Create database if it doesn't exist
create_database_if_not_exists()

engine = create_engine(
    DATABASE_URL,
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
