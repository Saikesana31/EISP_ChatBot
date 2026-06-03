"""
app/database.py — database connection and session management

* Creates async SQLAlchemy engine + connection pool.
* Provides get_db() dependency to get a session in API routes.
* get_db_session() is a helper function to get a session for internal use .(context for Agent tools )

# why Async?
If we used a synchronous DB driver (like psycopg2), every DB query would BLOCK the 
event loop thread—meaning no other WebSocket messages or HTTP requests could be handled
while waiting for Postgresl to respond.

asyncpg is an async DB driver that allows us to run DB queries without blocking the event loop.
This means we can handle multiple WebSocket messages and HTTP requests concurrently,
even while waiting for DB responses.

* engine              the connection pool (shared across the whole app)
* AsyncSessionLocal   factory to create individual sessions per request
* get_db()            FastAPI dependency: creates session, commits, closes
* get_db_session()    context manager version for use outside FastAPI routes
                      (used inside agent tools and service methods)
    
"""

from __future__ import annotations
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker,AsyncEngine
from app.config import get_settings
from typing import AsyncGenerator

settings = get_settings()

# Create the async SQLAlchemy engine (connection pool)
engine : AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.debug,                          # Set to True for SQL query logging
    pool_pre_ping=True,                           # Check if connections are alive before using them
    pool_size=settings.database_pool_size,        # keep a pool of 10 connections open
    max_overflow=settings.database_max_overflow,  # Allow temporary connections above pool_size(upto 20 more)
)

# Create a session factory that will generate new sessions for each request
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (optional)
    autoflush = False        # Don't automatically flush changes to the DB before queries (optional)
)

# FastAPI dependency to get a DB session for each request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session for each request.
    It creates a new session, yields it to the route handler, and ensures
    that the session is committed and closed after the request is done.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit changes if no exceptions occurred
        except Exception:
            await session.rollback()  # Rollback on error
            raise
        finally:
            await session.close()   # Ensure the session is closed
            

# Context manager for getting a DB session outside of FastAPI routes (e.g., in agent tools)
@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager to provide a database session for internal use (e.g., in agent tools).
    It creates a new session, yields it for use, and ensures that the session is committed and closed.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit changes if no exceptions occurred
        except Exception:
            await session.rollback()  # Rollback on error
            raise
        finally:
            await session.close()   # Ensure the session is closed
