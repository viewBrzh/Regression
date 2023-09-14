from pydantic import BaseModel

class WineDataBase(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    quality: float

class WineDataPredictBase(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

class WineDataCreate(WineDataBase):
    pass

class WineDataUpdate(WineDataBase):
    pass

class WineData(WineDataBase):
    id: int

    class Config:
        orm_mode = True

