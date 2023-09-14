from fastapi import FastAPI
import api.redwine as regression
import api.redwine_view as regression_view
import api.redwine_train as regression_train

app = FastAPI()
app.include_router(regression.router)
app.include_router(regression_view.router)
app.include_router(regression_train.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
