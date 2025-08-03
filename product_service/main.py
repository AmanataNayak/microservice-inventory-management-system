from fastapi import FastAPI
from database import Base, engine
from router import product_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhostL3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(product_router)

@app.get("/")
def index():
    return {
        "message": "Hello world"
    }