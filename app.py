from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import io
import board
import adafruit_ahtx0
from picamera2 import Picamera2
from PIL import Image

app = FastAPI()

# Static Files (Frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# CORS erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DHT20 Sensor (AHT20 kompatibel) Setup ---
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

# --- Kamera Setup ---
camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start()

# --- API Endpunkte ---

@app.get("/api/sensor")
def read_sensor():
    try:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        return {"temperature": temperature, "humidity": humidity}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/camera")
def get_camera_image():
    image = camera.capture_array()
    img = Image.fromarray(image)

    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)

    return FileResponse(buf, media_type="image/jpeg", filename="camera.jpg")
