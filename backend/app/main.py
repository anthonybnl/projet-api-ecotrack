from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.city import router as city_router
from app.routers.measurement import router as measurement_router
from app.routers.users import router as user_router
from app.routers.stats import router as stats_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(city_router)
app.include_router(measurement_router)
app.include_router(user_router)
app.include_router(stats_router)


@app.get("/health")
def healthcheck():
    return {
        "status": "up",
    }
