import uvicorn
import src.database as database
from fastapi import FastAPI
from src.routers import users

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users, i.e., login and registration.",
    },
]


app = FastAPI(openapi_tags=tags_metadata)
database.init_db()


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
