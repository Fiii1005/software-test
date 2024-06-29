from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from services import user as user_service
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas import schemas
from schemas.schemas import UserInDB, UserOut
from utils.database import get_db
from models.models import User
from typing import List

from schemas.schemas import UserUpdatePassword


# 获取请求的远程地址
limiter = Limiter(key_func=get_remote_address)

# 创建路由实例
user = APIRouter()

# 响应模型
# 定义一个POST请求的路由，路径为‘/register’
@user.post('/register', response_model=schemas.User)
# 限制10分钟最多被访问10次
@limiter.limit("10/10minutes")
# 异步函数register，处理用户注册请求
async def register(request: Request,
                   user: schemas.UserCreate,
                   db: Session = Depends(get_db)):
    print(user)
    user.username = user.username.lower()
    user = user_service.create_user(db, user)
    # 返回响应函数值
    return user

# 登录界面
@user.post('/login', response_model=schemas.Token)
@limiter.limit("10/minute")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends() # 依赖项，表单数据，用于获取用户名和密码
):
    # 用户名转小写
    username = form_data.username.lower()
    password = form_data.password
    form = await request.form()  # 首先获取完整的表单数据
    role = form.get('role')  # 然后从表单数据中提取 'role' 字段

    token = user_service.login(db, username, password, role)
    if token == "WRONG_PASSWORD":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif token == "WRONG_ROLE":
        raise HTTPException(status_code=400, detail="Incorrect role")
    return schemas.Token(access_token=token, token_type="bearer")



# # 获取用户数据
# @user.get('/users', response_model=dict)
# @limiter.limit("10/minute")
# async def get_users(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     users = db.query(User).offset(skip).limit(limit).all()
#     total = db.query(User).count()
#     return {"list": [schemas.UserOut.from_orm(user) for user in users], "pageTotal": total}


# 获取用户数据
@user.get('/users', response_model=dict)
@limiter.limit("10/minute")
async def get_users(request: Request, skip: int = 0, limit: int = 10, username: str | None = None, db: Session = Depends(get_db)):
    query = db.query(User)
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    users = query.offset(skip).limit(limit).all()
    total = query.count()
    return {"list": [schemas.UserOut.from_orm(user) for user in users], "pageTotal": total}



# 创建新用户
@user.post('/users', response_model=schemas.UserOut)
@limiter.limit("10/10minutes")
async def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_user

# 更新用户
@user.put('/users/{user_id}', response_model=schemas.UserOut)
@limiter.limit("10/10minutes")
async def update_user(request: Request, user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 删除用户
@user.delete('/users/{user_id}', response_model=schemas.UserOut)
@limiter.limit("10/10minutes")
async def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user.put("/users/{username}/password", response_model=dict)
async def update_password(username: str, user_update: UserUpdatePassword, db: Session = Depends(get_db)):
    try:
        await user_service.update_user_password(db, username, user_update.old_password, user_update.new_password)
        return {"status": "success"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


