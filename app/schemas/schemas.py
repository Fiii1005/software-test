#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# 用户注册响应函数
class UserBase(BaseModel):
    user_id: int | None = None # 可选的
    gender: str | None = None
    age: int | None = None
    phone_number: str | None = None
    
    username: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=5)
    email: EmailStr
    role: str


class User(UserBase):
    class Config:
        from_attributes = True


class UserInDB(UserBase):
    encoded_password: str

    class Config:
        from_attributes = True


# 用户注册查询
class UserCreate(UserBase):
    username: str = Field(pattern=r'^[A-Za-z][A-Za-z0-9_]{5,15}$')
    email: EmailStr
    password: str
    role: str

class UserUpdate(BaseModel):
    username: str
    password: str 
    phone_number: str | None = None
    email: str
    role: str
    name: str | None = None
    gender: str | None = None
    age: int | None = None

class UserOut(BaseModel):
    user_id: int
    username: str
    password: str
    email: str
    role: str
    phone_number: str | None = None
    name: str | None = None
    gender: str | None = None
    age: int | None = None

    class Config:
        from_attributes = True



class LoginInfo(BaseModel):
    username: str
    password: str
    role: str

# 登录响应模型
class Token(BaseModel):
    access_token: str
    token_type: str


class UploadToken(BaseModel):
    upload_token: str
    
    
class ChatInfo(BaseModel):
    message: str
    status: str | None = None
    
    
class ChatCreate(BaseModel):
    prompt: str

class MessageOut(BaseModel):
    msg_id: int
    user_id: int
    message: str
    status: str
    date: str

    class Config:
        from_attributes = True


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str
