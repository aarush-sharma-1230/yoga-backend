from fastapi import APIRouter, Depends, Request

router = APIRouter()


@router.get("/health")
async def health():
  return {"status": "ok"}
