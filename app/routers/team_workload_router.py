from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.team_model import Team
from app.models.consultation_schedule import ConsultationSchedule

router = APIRouter(prefix="/teams/workload", tags=["Team Workload Analytics"])


# ---------------------------------------------------------
# 1. Workload summary for all teams
# ---------------------------------------------------------
@router.get("/summary")
def workload_summary(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    now = datetime.utcnow()

    summary = []

    for team in teams:
        upcoming = db.query(ConsultationSchedule).filter(
            ConsultationSchedule.team_id == team.id,
            ConsultationSchedule.scheduled_time > now
        ).count()

        past = db.query(ConsultationSchedule).filter(
            ConsultationSchedule.team_id == team.id,
            ConsultationSchedule.scheduled_time < now
        ).count()

        summary.append({
            "team_id": team.id,
            "team_name": team.name,
            "upcoming_consultations": upcoming,
            "past_consultations": past,
            "total_consultations": upcoming + past
        })

    return summary


# ---------------------------------------------------------
# 2. Workload for a specific team
# ---------------------------------------------------------
@router.get("/{team_id}")
def team_workload(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    now = datetime.utcnow()

    upcoming = db.query(ConsultationSchedule).filter(
        ConsultationSchedule.team_id == team_id,
        ConsultationSchedule.scheduled_time > now
    ).all()

    past = db.query(ConsultationSchedule).filter(
        ConsultationSchedule.team_id == team_id,
        ConsultationSchedule.scheduled_time < now
    ).all()

    return {
        "team_id": team.id,
        "team_name": team.name,
        "upcoming_consultations": upcoming,
        "past_consultations": past,
        "total_consultations": len(upcoming) + len(past)
    }


# ---------------------------------------------------------
# 3. Identify busiest team
# ---------------------------------------------------------
@router.get("/busiest")
def busiest_team(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    now = datetime.utcnow()

    busiest = None
    max_load = -1

    for team in teams:
        load = db.query(ConsultationSchedule).filter(
            ConsultationSchedule.team_id == team.id,
            ConsultationSchedule.scheduled_time > now
        ).count()

        if load > max_load:
            max_load = load
            busiest = team

    if not busiest:
        return {"message": "No teams have scheduled consultations"}

    return {
        "team_id": busiest.id,
        "team_name": busiest.name,
        "upcoming_consultations": max_load
    }


# ---------------------------------------------------------
# 4. Identify free team (no upcoming consultations)
# ---------------------------------------------------------
@router.get("/free")
def free_team(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    now = datetime.utcnow()

    free_teams = []

    for team in teams:
        upcoming = db.query(ConsultationSchedule).filter(
            ConsultationSchedule.team_id == team.id,
            ConsultationSchedule.scheduled_time > now
        ).count()

        if upcoming == 0:
            free_teams.append(team)

    return {
        "free_teams": [{"id": t.id, "name": t.name} for t in free_teams],
        "count": len(free_teams)
    }
