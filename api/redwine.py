from fastapi import APIRouter, HTTPException
from database import db_cursor, db_connection
from models.redwine import WineData, WineDataCreate, WineDataUpdate  # Assuming you have WineData models

router = APIRouter()

@router.get("/redwine/", response_model=list[WineData])
def read_all_wine_data():
    query = "SELECT * FROM redwine ORDER BY id DESC LIMIT 20"
    db_cursor.execute(query)
    rows = db_cursor.fetchall()

    wine_data_list = []
    column_names = [column[0] for column in db_cursor.description]
    for row in rows:
        wine_data_dict = dict(zip(column_names, row))
        wine_data_list.append(WineData(**wine_data_dict))

    return wine_data_list

@router.get("/redwine/{data_id}", response_model=WineData)
def read_wine_data(data_id: int):
    query = "SELECT * FROM redwine WHERE id = %s"
    db_cursor.execute(query, (data_id,))
    row = db_cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Data not found")

    wine_data_dict = dict(zip(db_cursor.column_names, row))
    return WineData(**wine_data_dict)

@router.post("/redwine/", response_model=WineData)
def create_wine_data(data: WineDataCreate):
    query = """
    INSERT INTO redwine (
        `fixed_acidity`, `volatile_acidity`, `citric_acid`, `residual_sugar`, 
        `chlorides`, `free_sulfur_dioxide`, `total_sulfur_dioxide`, `density`, 
        `pH`, `sulphates`, `alcohol`, `quality`
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    values = (
        data.fixed_acidity, data.volatile_acidity, data.citric_acid, data.residual_sugar,
        data.chlorides, data.free_sulfur_dioxide, data.total_sulfur_dioxide, data.density,
        data.pH, data.sulphates, data.alcohol, data.quality
    )

    db_cursor.execute(query, values)
    db_connection.commit()

    wine_data_id = db_cursor.lastrowid  # Get the auto-generated id
    return WineData(id=wine_data_id, **data.dict())

@router.put("/redwine/{data_id}", response_model=WineData)
def update_wine_data(data_id: int, updated_data: WineDataUpdate):
    query = """
        UPDATE redwine
        SET 
            `fixed_acidity` = %s, 
            `volatile_acidity` = %s, 
            `citric_acid` = %s, 
            `residual_sugar` = %s,
            `chlorides` = %s, 
            `free_sulfur_dioxide` = %s, 
            `total_sulfur_dioxide` = %s,
            `density` = %s, 
            `pH` = %s, 
            `sulphates` = %s, 
            `alcohol` = %s, 
            `quality` = %s
        WHERE id = %s
    """
    values = (
        updated_data.fixed_acidity, updated_data.volatile_acidity, updated_data.citric_acid,
        updated_data.residual_sugar, updated_data.chlorides, updated_data.free_sulfur_dioxide,
        updated_data.total_sulfur_dioxide, updated_data.density, updated_data.pH,
        updated_data.sulphates, updated_data.alcohol, updated_data.quality, data_id
    )

    db_cursor.execute(query, values)
    db_connection.commit()

    updated_data_dict = updated_data.dict()
    updated_data_dict["id"] = data_id
    return WineData(**updated_data_dict)

@router.delete("/redwine/{data_id}", response_model=WineData)
def delete_wine_data(data_id: int):
    query = "SELECT * FROM redwine WHERE id = %s"
    db_cursor.execute(query, (data_id,))
    row = db_cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Data not found")

    deleted_wine_data = dict(zip(db_cursor.column_names, row))

    delete_query = "DELETE FROM redwine WHERE id = %s"
    db_cursor.execute(delete_query, (data_id,))
    db_connection.commit()

    return deleted_wine_data
