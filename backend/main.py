from fastapi import FastAPI
from auth.auth_router import router as auth_router
# from policy.policy_engine import router as policy_router

app = FastAPI(title="ZTA System")

app.include_router(auth_router)
# app.include_router(policy_router)

@app.get("/")
def root():
    return {"status": "ZTA Backend Running"}