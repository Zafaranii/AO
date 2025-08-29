# Example router
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from database import get_db
# from schemas.user import UserCreate, UserUpdate, UserResponse
# from crud import user as crud_user

# router = APIRouter(
#     prefix="/users",
#     tags=["users"]
# )

# @router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already registered"
#         )
#     return crud_user.create_user(db=db, user=user)

# @router.get("/", response_model=List[UserResponse])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud_user.get_users(db, skip=skip, limit=limit)
#     return users

# @router.get("/{user_id}", response_model=UserResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.put("/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     db_user = crud_user.update_user(db, user_id=user_id, user=user)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.delete("/{user_id}", response_model=UserResponse)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud_user.delete_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# Add your API routes here
