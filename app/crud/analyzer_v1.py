from sqlalchemy.orm import Session
from sqlalchemy import text

def run_analysis(db: Session, data: dict):
    return {"message": "Analyzer v1 executed", "input": data}

def get_devices(db: Session):
    result = db.execute(text("SELECT * FROM devices")).mappings().all()
    return list(result)

def get_device(db: Session, device_id: int):
    result = db.execute(
        text("SELECT * FROM devices WHERE device_id = :id"),
        {"id": device_id}
    ).mappings().first()
    return result

def get_outputs(db: Session):
    result = db.execute(text("SELECT * FROM device_outputs")).mappings().all()
    return list(result)

def get_output(db: Session, device_id: int):
    result = db.execute(
        text("SELECT * FROM device_outputs WHERE device_id = :id"),
        {"id": device_id}
    ).mappings().first()
    return result

def get_full_device(db: Session, device_id: int):
    device = get_device(db, device_id)
    output = get_output(db, device_id)
    return {"device": device, "output": output}

def compute_values(db: Session, device_id: int):
    return {"device_id": device_id, "computed": True}
