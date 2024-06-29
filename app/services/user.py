#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import secrets
from typing import Union, Type, Optional

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

import config
from crud import user as crud
from models.models import User
from schemas.schemas import UserInDB, UserCreate
from utils import security, database
from utils.security import encode_password, verify_password

# 数据库比较登录操作
def login(db: Session, username: str, plain_password: str,user_role:str) -> str | None:
    """
    Generate access token.
    :param db: SQLAlchemy.Session
    :param username
    :param plain_password:
    :return:
    """
    # 获得用户名
    user: User = crud.get_user(db, username)
    if user:
        # if not user.is_active:
            # raise HTTPException(status_code=400, detail="Inactivated user")
            # 验证密码（明文密码、数据库中密码）
        if security.verify_password(plain_password, user.password) == False:
            return "WRONG_PASSWORD"
        if user.role != user_role:
            return "WRONG_ROLE"
        # 如果验证成功，设置令牌
        return security.generate_access_jwt(username, config.TOKEN_EXPIRE_MINUTES)
    return None


async def get_current_user_or_none(db: Session = Depends(database.get_db),
                                   token: str = Depends(security.optional_oauth2_scheme)) -> Optional[UserInDB]:
    username = security.extract_username(token)
    if username is None:
        return None
    user = await crud.get_user(db, username)
    return user if user and user.is_active else None


async def get_current_user(db: Session = Depends(database.get_db),
                           token: str = Depends(security.oauth2_scheme)) -> UserInDB:
    """
    For view functions to get current authorized user.
    :param db: SQLAlchemy.Session
    :param token: FastAPI Depends
    :return:
    """
    username = security.extract_username(token)
    return await crud.get_active_user(db, username)


def create_user(db: Session, user: UserCreate) -> User:
    """
    在数据库中创建一个新用户
    参数：
    db：数据库操作
    user：包含了创建用户所需信息
    ->User：返回值
    """
    # 实际的数据库操作
    user: User | None = crud.create_user(db, user)
    if user is None:
        raise HTTPException(status_code=400, detail="Username has already existed")
    return user

def update_user(db: Session, username: str, user: UserCreate) -> User:
    """
    更新用户信息
    :param db: 数据库操作
    :param username: 用户名
    :param user: 包含了更新用户所需信息
    :return: 返回值
    """
    user: User | None = crud.update_user(db, username, user)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user

# 删除用户
def delete_user(db: Session, user_id: int) -> Optional[User]:
    """
    删除用户
    :param db: 数据库操作
    :param user_id: 用户id
    :return: 返回值
    """
    user: User | None = crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user


def refresh_upload_token(db: Session, username: str) -> str:
    user: Type[User] = db.query(User).filter(User.username == username).one()
    user.upload_token = secrets.token_hex(32)
    db.commit()
    db.refresh(user)

    return user.upload_token


async def update_user_password(db: Session, username: str, old_password: str, new_password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    hashed_new_password = encode_password(new_password)
    await crud.update_user_password(db, username, hashed_new_password)