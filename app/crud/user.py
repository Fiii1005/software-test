from typing import Optional

from sqlalchemy.orm import Session

from schemas import schemas
from models.models import User
from utils import security


def get_user(db: Session, username: str) -> Optional[User]:
    db_user = db.query(User).filter(User.username == username).first()
    return db_user

# 用于在数据库中创建一个新用户
def create_user(db: Session, user: schemas.UserCreate) -> Optional[User]:
    # 首先检查用户名是否已经存在，如果存在返回None
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return None
    db_user = User(
        username=user.username,
        password=security.encode_password(user.password),
        name=None,
        gender=None,
        age=None,
        phone_number = None,
        email = user.email,
        role = user.role,
    )
    # 数据库提交请求
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 更新用户信息
def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[User]:
    # 查找现有用户
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        return None

    # 更新用户信息
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password = security.encode_password(user.password)
    if user.phone_number is not None:
        db_user.phone_number = user.phone_number
    if user.email is not None:
        db_user.email = user.email
    if user.role is not None:
        db_user.role = user.role
    if user.name is not None:
        db_user.name = user.name
    if user.gender is not None:
        db_user.gender = user.gender
    if user.age is not None:
        db_user.age = user.age

    # 提交更改
    db.commit()
    db.refresh(db_user)
    return db_user

# 删除用户
def delete_user(db: Session, user_id: int) -> Optional[User]:
    # 查找现有用户
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        return None

    # 删除用户
    db.delete(db_user)
    db.commit()
    return db_user



async def update_user_password(db: Session, username: str, hashed_new_password: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.password = hashed_new_password
        db.commit()
