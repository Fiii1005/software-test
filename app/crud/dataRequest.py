from sqlalchemy.orm import Session
from sqlalchemy import extract, func, asc
from typing import List
from schemas import data
from models import models
from fastapi import HTTPException
from datetime import datetime

def get_water_physic_data(db: Session, station_id: str, data_time: str | None = None) -> List[data.waterPhysicOut]:
    data_list=[]
    if data_time:
        data_list = db.query(models.water_physic).filter(models.water_physic.station_id == station_id,
                                                         models.water_physic.time == data_time).all()
    else:
        data_list = db.query(models.water_physic).filter(
            models.water_physic.station_id == station_id).all()
    if not data_list:
        raise HTTPException(status_code=404, detail="Water physic data not found")
    
    # 将 datetime 类型的时间字段转换为字符串类型
    for data_entry in data_list:
        data_entry.time = data_entry.time.strftime("%Y-%m-%d %H:%M:%S")
    
    return data_list

def create_water_physic_data(db: Session, water_data: data.waterPhysicUploadIn) -> data.waterPhysicUploadOut:
    # 创建一个新的水体物理数据对象
    new_water_data = models.water_physic(
        station_id=water_data.station_id,
        time=water_data.time,
        depth=water_data.depth,
        temperature=water_data.temperature,
        transparency=water_data.transparency,
        solids=water_data.solids,
        electrical_conductivity=water_data.electrical_conductivity
    )
    
    # 将新的水体物理数据对象添加到数据库中
    db.add(new_water_data)
    db.commit()
    db.refresh(new_water_data)
    
    # 返回上传结果
    return data.waterPhysicUploadOut(
        response="Data uploaded successfully")

def get_water_chemistry_data(db: Session, station_id: str, data_time: str | None = None) -> List[data.waterChemistryOut]:
    data_list=[]
    if data_time:
        print("have data time")
        data_list = db.query(models.water_chemistry).filter(models.water_chemistry.station_id == station_id,
                                                            models.water_chemistry.time == data_time).all()
    else:
        data_list = db.query(models.water_chemistry).filter(
            models.water_chemistry.station_id == station_id).all()
    if not data_list:
        raise HTTPException(status_code=404, detail="Water chemistry data not found")
    
    # 将 datetime 类型的时间字段转换为字符串类型
    for data_entry in data_list:
        data_entry.time = data_entry.time.strftime("%Y-%m-%d %H:%M:%S")
    
    return data_list

# 获取鱼群每年的数量
def get_fish_number(db: Session, fishType: str) -> data.fishnumberOut:
    # 查询数据库，按年份汇总鱼类数量
    annual_totals = (
        db.query(extract('year', models.fish.date).label('year'), func.sum(models.fish.num).label('total_num'))
        .filter(models.fish.fishname == fishType)
        .group_by(extract('year', models.fish.date))
        .all()
    )
    
    if not annual_totals:
        raise HTTPException(status_code=404, detail="No fish data found")
    
    # 提取年份和总数
    categories = [str(year) for year, _ in annual_totals]
    cdata = [int(total_num) for _, total_num in annual_totals]
    
    # 创建并返回结果模型
    result = data.fishnumberOut(categories=categories, data=cdata)
    
    return result


# 排序函数
def custom_sort_key(lengthrange):
    # 定义自定义排序的规则，例如将 "0-3" 转换为数字 0，"3-6" 转换为数字 3，依此类推
    start_num = float(lengthrange.split('-')[0])
    return start_num

def get_fish_weightrange(db: Session, fishname: str,placetype: str) -> data.fish_chartdataOut:
    # 查询数据库，获取指定鱼类的所有长度范围及其对应的数量，并进行分组和合并
    fish_data = []
    if(placetype=='1'):
        fish_data = (
        db.query(models.fish.weightrange, func.sum(models.fish.num).label('num'))
        .filter(models.fish.fishname == fishname)
        .group_by(models.fish.weightrange)
        .all()
        )
    else:
        fish_data = (
        db.query(models.fish_2.weightrange, func.sum(models.fish_2.num).label('num'))
        .filter(models.fish_2.fishname == fishname)
        .group_by(models.fish_2.weightrange)
        .all()
        )
    
    if not fish_data:
        raise HTTPException(status_code=404, detail="No data found for the specified fish type")
    
    # 对结果按照自定义排序规则排序
    fish_data = sorted(fish_data, key=lambda x: custom_sort_key(x[0]))

    # 准备输出数据
    categories = [weightrange for weightrange, _ in fish_data]
    cdata = [int(num) for _, num in fish_data]
    
    result = data.fish_chartdataOut(categories=categories, data=cdata)
    
    return result

def get_fish_lengthrange(db: Session, fishname: str, placetype: str) -> data.fish_chartdataOut:
    # 查询数据库，获取指定鱼类的所有体重范围及其对应的数量，并进行分组和合并
    fish_data = []
    if(placetype=='1'):
        fish_data = (
        db.query(models.fish.lengthrange, func.sum(models.fish.num).label('num'))
        .filter(models.fish.fishname == fishname)
        .group_by(models.fish.lengthrange)
        .all()
        )
    else:
        fish_data = (
        db.query(models.fish_2.lengthrange, func.sum(models.fish_2.num).label('num'))
        .filter(models.fish_2.fishname == fishname)
        .group_by(models.fish_2.lengthrange)
        .all()
        )
    
    if not fish_data:
        raise HTTPException(status_code=404, detail="No data found for the specified fish type")
    
    # 对结果按照自定义排序规则排序
    fish_data = sorted(fish_data, key=lambda x: custom_sort_key(x[0]))

    # 准备输出数据
    categories = [lengthrange for lengthrange, _ in fish_data]
    cdata = [int(num) for _, num in fish_data]
    
    result = data.fish_chartdataOut(categories=categories, data=cdata)
    
    return result

def get_fish_daynumber(db: Session) -> data.dashOpt1Out:
    # 查询数据库，按日期汇总鱼类数量
    annual_totals = (
        db.query(models.fish.date, func.sum(models.fish.num).label('total_num'))
        .filter(models.fish.date >= datetime(2022, 1, 1))  # 开始日期设定为2018年1月1日
        .filter(models.fish.date <= datetime(2023, 12, 31))  # 结束日期设定为2023年12月31日
        .group_by(models.fish.date)
        .all()
    )
    
    if not annual_totals:
        raise HTTPException(status_code=404, detail="No fish data found")
    
    # 提取日期和总数
    categories = [str(date) for date, _ in annual_totals]
    data1 = [int(total_num) for _, total_num in annual_totals]
    
    # 创建并返回结果模型
    result = data.dashOpt1Out(categories=categories, data1=data1)
    
    return result

def get_dashOpt2(db: Session)->data.dashOpt2Out:
    # 查询数据库，按日期汇总鱼类数量
    annual_totals = (
        db.query(models.fish.fishname, func.sum(models.fish.num).label('total_num'))
        .filter(models.fish.date >= datetime(2015, 1, 1))  # 开始日期设定为2023年1月1日
        .filter(models.fish.date <= datetime(2015, 12, 31))  # 结束日期设定为2023年12月31日
        .group_by(models.fish.fishname)
        .all()
    )
        
    if not annual_totals:
        raise HTTPException(status_code=404, detail="No fish data found")
    # 构建 FishData 实例列表
    fish_data_list = [
        data.FishData(name=name[:3], value=int(total_num)) for name, total_num in annual_totals
    ]
    # 创建并返回结果模型
    result = data.dashOpt2Out(data=fish_data_list)
    
    return result