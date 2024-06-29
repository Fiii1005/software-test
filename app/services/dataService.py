from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from schemas import data
from crud import dataRequest as crud

def search_water_physic_data(db: Session, waterRdata: data.waterPhysicIn) -> List[data.waterPhysicOut]:
    """
    在数据库中根据站点ID和日期搜索水体物理数据
    参数：
    db：数据库操作
    station_id：站点ID
    date：日期
    返回值：
    List[WaterPhysicData]：符合搜索条件的水体物理数据列表
    """
    # 实际的数据库操作

    if waterRdata.time:
        return crud.get_water_physic_data(db, waterRdata.station_id, waterRdata.time)
    else:
        return crud.get_water_physic_data(db, waterRdata.station_id)

def upload_water_physic_data(db: Session, waterUdata: data.waterPhysicUploadIn) -> data.waterPhysicUploadOut:
    """
    上传水体物理数据到数据库中
    参数：
    db：数据库操作
    waterUdata：要上传的水体物理数据
    返回值：
    waterPhysicOut：上传的水体物理数据
    """
    return crud.create_water_physic_data(db, waterUdata)

def search_water_chemistry_data(db: Session, waterRdata: data.waterChemistryIn) -> List[data.waterChemistryOut]:
    """
    在数据库中根据站点ID和日期搜索水体化学数据
    参数：
    db：数据库操作
    station_id：站点ID
    date：日期
    返回值：
    List[WaterChemistryData]：符合搜索条件的水体化学数据列表
    """
    # 实际的数据库操作

    if waterRdata.time:
        return crud.get_water_chemistry_data(db, waterRdata.station_id, waterRdata.time)
    else:
        return crud.get_water_chemistry_data(db, waterRdata.station_id)
    
def search_ranks(db: Session)->data.ranksOut:
    date="2001-01-01"
    station_id="THL00"
    physic_data=crud.get_water_physic_data(db,station_id,date)[0]
    chemistry_data=crud.get_water_chemistry_data(db,station_id,date)[0]
    """
    result=data.ranksOut(
        salinity=chemistry_data.kmno4,
        dissolved_o=chemistry_data.dissolved_o,
        ph=chemistry_data.pH,
        water_tem=physic_data.temperature
    )
    """
    result=[chemistry_data.kmno4,chemistry_data.dissolved_o,chemistry_data.pH,physic_data.temperature]
    return result

def search_fishnumber(db: Session, fishType: str)->data.fishnumberOut:
    return crud.get_fish_number(db, fishType)

def search_fish_chartdata(db: Session,fish_chartdata: data.fish_chartdataIn)->data.fish_chartdataOut:
    if fish_chartdata.type=="weight":
        return crud.get_fish_weightrange(db,fish_chartdata.fishtype,placetype=fish_chartdata.placetype)
    elif fish_chartdata.type=="size":
        return crud.get_fish_lengthrange(db,fish_chartdata.fishtype,placetype=fish_chartdata.placetype)
    
def search_fish_daynumber(db: Session)->data.dashOpt1Out:
    return crud.get_fish_daynumber(db)

def search_dashOpt2(db: Session)->data.dashOpt2Out:
    return crud.get_dashOpt2(db)