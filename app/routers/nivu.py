from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_active_user

router = APIRouter(
    prefix="/nivu",
    tags=["nivu"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=["nivu"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
