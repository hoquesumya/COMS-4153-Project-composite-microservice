from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers import stydylinkcompo

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


app.include_router(stydylinkcompo.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)