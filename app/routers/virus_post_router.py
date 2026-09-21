from fastapi import APIRouter

router = APIRouter()

@router.get("/virus/post")
def virus_post_test():
    return {"message": "virus_post_router is working"}
