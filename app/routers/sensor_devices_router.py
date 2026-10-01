from fastapi import APIRouter

router = APIRouter(prefix="/sensor-devices", tags=["Sensor Devices"])

@router.get("/")
def sensor_devices_info():
    return {
        "title": "Sensor Devices",
        # Updated to point to your Vercel frontend public folder
        "image_url": "https://ai-biosensing-frontend-v2.vercel.app/device.png",
        "content": [
            "The sensor devices demonstrated in our MLDrift simulation represent the foundational version of our patented low‑grade biosensing technology. These devices are engineered to detect analytes at picogram‑level sensitivity, forming the baseline capability of our broader Piezo‑Pico to Femtotechnology Sensors Inc. platform.",
            
            "All sensor devices showcased in this dashboard are proprietary products owned exclusively by Piezo‑Pico to Femtotechnology Sensors Inc. The technology, design, firmware, and biosensing mechanisms are protected under active intellectual property rights.",
            
            "Any attempt to sell, distribute, replicate, or purchase similar devices from unauthorized sources is strictly prohibited. Unauthorized reproduction, resale, or reverse engineering of our patented biosensing technology will be subject to legal action under applicable statutes.",
            
            "By accessing this dashboard, customers acknowledge that the sensor devices and associated ML simulation tools are proprietary assets of Piezo‑Pico to Femtotechnology Sensors Inc. All commercial transactions must occur through our official marketplace."
        ]
    }
