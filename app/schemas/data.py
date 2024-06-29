from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from fastapi import UploadFile

class waterPhysicIn(BaseModel):
    station_id: str
    time: str | None = None

class waterPhysicOut(BaseModel):
    station_id: str
    time: str
    depth: float
    temperature: float
    transparency: float
    solids: float
    electrical_conductivity: int

class waterPhysicUploadIn(waterPhysicOut):
    None

class waterPhysicUploadOut(BaseModel):
    response: str

class waterChemistryIn(BaseModel):
    station_id: str
    time: str | None = None

class waterChemistryOut(BaseModel):
    station_id: str
    time: str
    pH: float
    total_N: float
    total_P: float
    chlorophyll: float
    chl_without_Mg: float
    kmno4: float
    dissolved_o: float
    BOD5: float
    NH4N: float
    HNO2: float
    NO3: float
    dissolved_N: float
    phosphate: float
    dissolved_P: float
    alkalinity: float
    potassium_lon: float
    sodium_lon: float
    calcium_lon: float
    magnesium_lon: float
    fluoride_lon: float
    chloride: float
    sulfate: float
    silicate: float
    alkalinity_as_caco3: float
    silicate_as_si: float

class ranksOut(BaseModel):
    salinity: float
    dissolved_o: float
    ph: float
    water_tem: float

class fishnumberOut(BaseModel):
    categories: list
    data: list

class fish_chartdataIn(BaseModel):
    type: str
    fishtype: str
    placetype: str

class fish_chartdataOut(BaseModel):
    categories: list
    data: list

class dashOpt1Out(BaseModel):
    categories: list
    data1: list

class FishData(BaseModel):
    value: int
    name: str

class dashOpt2Out(BaseModel):
    data: List[FishData]


# Equipment
class EquipmentBase(BaseModel):
    equipment_type: str
    equipment_id: str
    equipment_status: str
    equipment_longitude: float
    equipment_latitude: float
    equipment_last_maintenace: date
    equipment_next_maintenace: date
    equipment_warranty_expiry: date
    equipment_length: float
    equipment_width: float
    equipment_depth: float

class EquipmentUploadIn(EquipmentBase):
    pass

class EquipmentUploadOut(BaseModel):
    response: str

class EquipmentOut(EquipmentBase):
    pass


class EquipmentLocationOut(BaseModel):
    equipment_id: str
    equipment_type: str
    equipment_longitude: float
    equipment_latitude: float


class MessageOut(BaseModel):
    id: int
    message: str
    status: str
    date: str

    class Config:
        from_attributes=True

class ImportData(BaseModel):
    file: UploadFile