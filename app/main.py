from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.health import health_router
from app.auth import auth_router
from app.query import query_router
from app.session import session_router
from app.sequence import sequence_router
from app.websocket import websocket_router
from app.database.mongo import MongoDB
from fastapi.responses import JSONResponse
from app.globals.errors import CustomException
from dotenv import load_dotenv
import os

app = FastAPI(title="Yoga API", version="1.0")
load_dotenv()
MongoDB()

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(health_router.router)
app.include_router(auth_router.router)
app.include_router(query_router.router)
app.include_router(session_router.router)
app.include_router(sequence_router.router)
app.include_router(websocket_router.router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
  return JSONResponse(
      status_code=500,
      content={"detail": f"{exc.name}"},
  )

# # Run: uvicorn app.main:app --reload
