#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Double, Date, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# 创建数据库用用户信息结构
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)  # 用户编号
    username = Column(String(255))  # 用户名
    password = Column(String(255))  # 密码
    name = Column(String(255))  # 姓名
    gender = Column(String(255))  # 性别
    age = Column(Integer)  # 年龄
    phone_number = Column(String(255))  # 电话号码
    email = Column(String(255))  # 邮箱地址
    role = Column(String(255))  # 职位

# 水质物理数据结构
class water_physic(Base):
    __tablename__ = 'water_physic'

    station_id = Column(String(255), primary_key=True) # 站点id
    time = Column(String(255), primary_key=True) # 数据记录时间
    depth = Column(Double) # 水体深度
    temperature = Column(Double) # 水温
    transparency = Column(Double) # 透明度
    solids = Column(Double) # 悬浮质
    electrical_conductivity = Column(Integer) # 电导率

# 保存水质化学数据
class water_chemistry(Base):
    __tablename__ = "water_chemistry"

    station_id=Column(String(255), primary_key=True) # 站点id
    time=Column(String(255), primary_key=True) # 数据记录时间
    pH=Column(Double) # pH值
    total_N=Column(Double) # 总氮
    total_P=Column(Double) # 总磷
    chlorophyll=Column(Double) # 叶绿素
    chl_without_Mg=Column(Double) # 去除镁的叶绿素
    kmno4=Column(Double) # 高锰酸盐指数
    dissolved_o=Column(Double) # 溶解氧
    BOD5=Column(Double) # 五日生化需氧量
    NH4N=Column(Double) # 氨氮
    HNO2=Column(Double) # 亚硝酸盐
    NO3=Column(Double) # 硝酸盐
    dissolved_N=Column(Double) # 溶解氮
    phosphate=Column(Double) # 磷酸盐
    dissolved_P=Column(Double) # 溶解磷
    alkalinity=Column(Double) # 碱度
    potassium_lon=Column(Double) # 钾离子
    sodium_lon=Column(Double) # 钠离子
    calcium_lon=Column(Double) # 钙离子
    magnesium_lon=Column(Double) # 镁离子
    fluoride_lon=Column(Double) # 氟离子
    chloride=Column(Double) # 氯离子
    sulfate=Column(Double) # 硫酸盐
    silicate=Column(Double) # 硅酸盐
    alkalinity_as_caco3=Column(Double) # 碳酸盐
    silicate_as_si=Column(Double) # 硅酸盐

class fish(Base):
    __tablename__ = "fish"

    date=Column(Date, primary_key=True) # 数据记录时间
    fishname=Column(String(255), primary_key=True) # 鱼类名称
    lengthrange=Column(String(255),primary_key=True) # 鱼类长度范围
    weightrange=Column(String(255),primary_key=True) # 鱼类体重范围
    num=Column(Integer) # 鱼类数量

class fish_2(Base):
    __tablename__ = "fish_2"

    date=Column(Date, primary_key=True) # 数据记录时间
    fishname=Column(String(255), primary_key=True) # 鱼类名称
    lengthrange=Column(String(255),primary_key=True) # 鱼类长度范围
    weightrange=Column(String(255),primary_key=True) # 鱼类体重范围
    num=Column(Integer) # 鱼类数量

# 保存设备信息
def equipment(Base):
    __tablename__ = "equipment"

    equipment_type=Column(String(255), primary_key=True) # 设备类型
    equipment_id=Column(String(255), primary_key=True) # 设备编号
    equipment_status=Column(String(255)) # 设备状态
    equipment_longitude=Column(Double) # 设备经度
    equipment_latitude=Column(Double) # 设备纬度
    equipment_last_maintenace=Column(Date) # 设备最后维护时间
    equipment_next_maintenace=Column(Date) # 设备下次维护时间
    equipment_warranty_expiry=Column(Date) # 设备保修到期时间
    equipment_length=Column(Double) # 设备长度
    equipment_width=Column(Double) # 设备宽度
    equipment_depth=Column(Double) # 设备深度

class Message(Base):
    __tablename__ = 'message'
    msg_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    message = Column(String)
    status = Column(String)
    date = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
