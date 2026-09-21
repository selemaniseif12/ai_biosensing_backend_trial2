from fastapi import APIRouter

router = APIRouter()

@router.get("/virus/count")
def virus_count_test():
    return {"count": 0}
