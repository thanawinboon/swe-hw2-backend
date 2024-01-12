import uvicorn
import src.database as database
from fastapi import FastAPI

app = FastAPI()
database.init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
