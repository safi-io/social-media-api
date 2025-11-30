from fastapi import FastAPI

from app.api.v1 import router as v1_router

app = FastAPI(title="API's for Social Media App.")


@app.get("/check", summary="Public Endpoint to Check the Server Health.")
async def check():
    return {"Status": "Good"}


# Register Routes
app.include_router(v1_router, prefix="/api/v1", tags=["Version 1 API"])
