from fastapi import APIRouter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.metrics import r2_score
from database import db_cursor, db_connection
from models.redwine import WineDataPredictBase  # Assuming you have a WineData model

router = APIRouter()

@router.get("/redwine_model/train")
async def train():
    wine_df = pd.read_sql("SELECT * FROM redwine", con=db_connection)
    
    X = wine_df.drop(["quality"], axis="columns")  # Assuming "quality" is the target column
    y = wine_df["quality"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    model_rf = RandomForestClassifier()
    model_rf.fit(X_train, y_train)

    with open('in_xgb', 'wb') as files:
        pickle.dump(model_rf, files)

    # make predictions on the test data
    yRF_predict = model_rf.predict(X_test)

    r2 = round(r2_score(y_test, yRF_predict), 3)

    return {"message": "in_xgb", "R2": str(r2)}

@router.post("/redwine_models/predict")
async def predict(item: WineDataPredictBase):
    # Create a dictionary to hold the input data
    input_data = {
        "fixed_acidity": [item.fixed_acidity],
        "volatile_acidity": [item.volatile_acidity],
        "citric_acid": [item.citric_acid],
        "residual_sugar": [item.residual_sugar],
        "chlorides": [item.chlorides],
        "free_sulfur_dioxide": [item.free_sulfur_dioxide],
        "total_sulfur_dioxide": [item.total_sulfur_dioxide],
        "density": [item.density],
        "pH": [item.pH],
        "sulphates": [item.sulphates],
        "alcohol": [item.alcohol]
    }

    # Load the trained model
    with open('in_xgb', 'rb') as model_file:
        model_rf = pickle.load(model_file)

    # Create a DataFrame from the input data
    wine_df = pd.DataFrame(input_data)
    
    # Make predictions using the loaded model
    quality_prediction = model_rf.predict(wine_df)
    
    # Convert the prediction to a Python native integer
    predicted_quality = int(quality_prediction[0])

    return {"quality": predicted_quality}
