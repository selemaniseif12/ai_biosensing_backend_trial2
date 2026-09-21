from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from calendar import monthrange

from app.database import get_db
from app.models.consultation_schedule import ConsultationSchedule
from app.models.team_model import Team

router = APIRouter(prefix="/calendar", tags=["Consultation Calendar"])


# ---------------------------------------------------------
# 1. Monthly calendar view
# ---------------------------------------------------------
@router.get("/month/{year}/{month}")
def calendar_month(year: int, month: int, db: Session = Depends(get_db)):
    start_date = datetime(year, month, 1)
    end_day = monthrange(year, month)[1]
    end_date = datetime(year, month, end_day, 23, 59, 59)

    schedules = db.query(ConsultationSchedule).filter(
        ConsultationSchedule.scheduled_time >= start_date,
        ConsultationSchedule.scheduled_time <= end_date
    ).all()

    # Group by day
    calendar_data = {}
    for schedule in schedules:
        day = schedule.scheduled_time.day
        calendar_data.setdefault(day, []).append(schedule)

    return {
        "year": year,
        "month": month,
        "days": calendar_data
    }


# ---------------------------------------------------------
# 2. Weekly calendar view
# ---------------------------------------------------------
@router.get("/week/{year}/{month}/{day}")
def calendar_week(year: int, month: int, day: int, db: Session = Depends(get_db)):
    start_date = datetime(year, month, day)
    end_date = start_date + timedelta(days=6)

    schedules = db.query(ConsultationSchedule).filter(
        ConsultationSchedule.scheduled_time >= start_date,
        ConsultationSchedule.scheduled_time <= end_date
    ).all()

    # Group by date
    week_data = {}
    for schedule in schedules:
        date_key = schedule.scheduled_time.date().isoformat()
        week_data.setdefault(date_key, []).append(schedule)

    return {
        "start": start_date.date(),
        "end": end_date.date(),
        "days": week_data
    }


# ---------------------------------------------------------
# 3. Daily agenda
# ---------------------------------------------------------
@router.get("/day/{year}/{month}/{day}")
def calendar_day(year: int, month: int, day: int, db: Session = Depends(get_db)):
    start_date = datetime(year, month, day)
    end_date = datetime(year, month, day, 23, 59, 59)

    schedules = db.query(ConsultationSchedule).filter(
        ConsultationSchedule.scheduled_time >= start_date,
        ConsultationSchedule.scheduled_time <= end_date
    ).all()

    return {
        "date": start_date.date(),
        "consultations": schedules
    }


# ---------------------------------------------------------
# 4. Team-specific calendar
# ---------------------------------------------------------
@router.get("/team/{team_id}/{year}/{month}")
def team_calendar(team_id: int, year: int, month: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    start_date = datetime(year, month, 1)
    end_day = monthrange(year, month)[1]
    end_date = datetime(year, month, end_day, 23, 59, 59)

    schedules = db.query(ConsultationSchedule).filter(
        ConsultationSchedule.team_id == team_id,
        ConsultationSchedule.scheduled_time >= start_date,
        ConsultationSchedule.scheduled_time <= end_date
    ).all()

    calendar_data = {}
    for schedule in schedules:
        day = schedule.scheduled_time.day
        calendar_data.setdefault(day, []).append(schedule)

    return {
        "team_id": team_id,
        "team_name": team.name,
        "year": year,
        "month": month,
        "days": calendar_data
    }
