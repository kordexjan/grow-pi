from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/sensor")
def read_sensor():
    # Dummy-Daten für Testzwecke
    return {"temperature": 23.5, "humidity": 40.2}

@app.get("/api/camera")
def get_camera_image():
    # Dummy-Fehlermeldung für Kamera (optional)
    return JSONResponse(content={"error": "Camera not connected (Testmode)"}, status_code=500)
