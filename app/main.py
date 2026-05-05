from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import encoders
from contextlib import asynccontextmanager

from app.health import health_router
from app.auth import auth_router
from app.query import query_router
from app.session import session_router
from app.sequence import sequence_router
from app.websocket import websocket_router
from app.database.mongo import MongoDB
from app.globals.exception_handlers import register_exception_handlers
from app.core.json_encoder import jsonable_encoder
from dotenv import load_dotenv

encoders.jsonable_encoder = jsonable_encoder


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create indexes for authentication collections."""

    db = MongoDB().get_database()
    await db["refresh_tokens"].create_index("token_hash", unique=True)
    await db["users"].create_index("google_sub", unique=True, sparse=True)
    yield


app = FastAPI(title="Yoga API", version="1.0", lifespan=lifespan)
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

register_exception_handlers(app)


# # Run: uvicorn app.main:app --reload
