from fastapi import FastAPI
from database import Base, engine
from routers import auth_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router)

@app.get("/")
def index():
    return {
        "message": "This is a auth service"
    }