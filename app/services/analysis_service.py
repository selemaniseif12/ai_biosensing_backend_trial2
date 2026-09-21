# app/services/analysis_service.py

from uuid import uuid4
from datetime import datetime
from app.models.analysis import Analysis

analysis_db = {}

def store_analysis(result):
    analysis_id = str(uuid4())
    entry = Analysis(id=analysis_id, **result)
    analysis_db[analysis_id] = entry
    return entry

def list_analysis():
    return list(analysis_db.values())

def get_analysis(analysis_id: str):
    return analysis_db.get(analysis_id)

def get_analysis_for_sample(sample_id: str):
    return [a for a in analysis_db.values() if a.sample_id == sample_id]

def get_analysis_for_measurement(measurement_id: str):
    return [a for a in analysis_db.values() if a.measurement_id == measurement_id]

def get_analysis_for_customer(customer_id: str):
    return [a for a in analysis_db.values() if a.customer_id == customer_id]

# ---------------------------------------------------------
# NEW: FILTER BY DATE RANGE
# ---------------------------------------------------------
def get_analysis_by_date_range(start_date: datetime, end_date: datetime):
    return [
        a for a in analysis_db.values()
        if start_date <= a.timestamp <= end_date
    ]

# ---------------------------------------------------------
# NEW: SORT ANALYSIS ENTRIES (NEWEST FIRST)
# ---------------------------------------------------------
def sort_analysis_newest_first(entries):
    return sorted(entries, key=lambda a: a.timestamp, reverse=True)

# ---------------------------------------------------------
# NEW: FILTER BY ANALYZER VERSION (V3, V4, V5, V6)
# ---------------------------------------------------------
def get_analysis_for_analyzer_version(version: str):
    return [
        a for a in analysis_db.values()
        if getattr(a, "analyzer_version", None) == version
    ]

# ---------------------------------------------------------
# NEW: FILTER BY VIRUS TYPE
# ---------------------------------------------------------
def get_analysis_for_virus(virus: str):
    return [
        a for a in analysis_db.values()
        if getattr(a, "virus", None) == virus
    ]

# ---------------------------------------------------------
# NEW: FILTER BY DEVICE ID
# ---------------------------------------------------------
def get_analysis_for_device(device_id: str):
    return [
        a for a in analysis_db.values()
        if getattr(a, "device_id", None) == device_id
    ]

# ---------------------------------------------------------
# NEW: COMBINED FILTER — DEVICE + VIRUS + DATE RANGE
# ---------------------------------------------------------
def get_analysis_combined(device_id: str, virus: str, start_date: datetime, end_date: datetime):
    results = []

    for a in analysis_db.values():
        if getattr(a, "device_id", None) != device_id:
            continue
        if getattr(a, "virus", None) != virus:
            continue
        if not (start_date <= a.timestamp <= end_date):
            continue

        results.append(a)

    return results

