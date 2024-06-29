from sqlalchemy.orm import Session
from sqlalchemy import extract, func, asc
from typing import List
from schemas import data
from models import models
from fastapi import HTTPException

# 获取设备数据
def get_equipment_data(db: Session, equipment_id: str, equipment_type: str | None = None) -> List[data.EquipmentOut]:
    data_list = []
    if equipment_type:
        data_list = db.query(models.Equipment).filter(
            models.Equipment.equipment_id == equipment_id,
            models.Equipment.equipment_type == equipment_type
        ).all()
    else:
        data_list = db.query(models.Equipment).filter(
            models.Equipment.equipment_id == equipment_id
        ).all()
    
    if not data_list:
        raise HTTPException(status_code=404, detail="Equipment data not found")
    
    # 将 datetime 类型的时间字段转换为字符串类型
    for data_entry in data_list:
        data_entry.equipment_last_maintenace = data_entry.equipment_last_maintenace.strftime("%Y-%m-%d")
        data_entry.equipment_next_maintenace = data_entry.equipment_next_maintenace.strftime("%Y-%m-%d")
        data_entry.equipment_warranty_expiry = data_entry.equipment_warranty_expiry.strftime("%Y-%m-%d")
    
    return data_list

# 创建设备数据
def create_equipment_data(db: Session, equipment_data: data.EquipmentUploadIn) -> data.EquipmentUploadOut:
    # 创建一个新的设备数据对象
    new_equipment_data = models.Equipment(
        equipment_type=equipment_data.equipment_type,
        equipment_id=equipment_data.equipment_id,
        equipment_status=equipment_data.equipment_status,
        equipment_longitude=equipment_data.equipment_longitude,
        equipment_latitude=equipment_data.equipment_latitude,
        equipment_last_maintenace=equipment_data.equipment_last_maintenace,
        equipment_next_maintenace=equipment_data.equipment_next_maintenace,
        equipment_warranty_expiry=equipment_data.equipment_warranty_expiry,
        equipment_length=equipment_data.equipment_length,
        equipment_width=equipment_data.equipment_width,
        equipment_depth=equipment_data.equipment_depth
    )
    
    # 将新的设备数据对象添加到数据库中
    db.add(new_equipment_data)
    db.commit()
    db.refresh(new_equipment_data)
    
    # 返回上传结果
    return data.EquipmentUploadOut(
        response="Data uploaded successfully")

# 获取设备地理位置信息
def get_equipment_location_map(db: Session, equipment_type: str) -> List[data.EquipmentLocationOut]:
    data_list = db.query(
        models.Equipment.equipment_id,
        models.Equipment.equipment_type,
        models.Equipment.equipment_longitude,
        models.Equipment.equipment_latitude
    ).filter(
        models.Equipment.equipment_type == equipment_type
    ).all()

    if not data_list:
        raise HTTPException(status_code=404, detail="No equipment of the specified type found")
    
    return [data.EquipmentLocationOut(
                equipment_id=item.equipment_id,
                equipment_type=item.equipment_type,
                equipment_longitude=item.equipment_longitude,
                equipment_latitude=item.equipment_latitude
            ) for item in data_list]
