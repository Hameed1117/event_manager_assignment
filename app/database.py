# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Keep the existing setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/appdb")
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Add the Database class that main.py expects
class Database:
    engine = None
    debug = False
    
    @classmethod
    def initialize(cls, database_url, debug=False):
        """Initialize the database connection."""
        cls.engine = create_async_engine(database_url, echo=debug)
        cls.debug = debug
    
    @classmethod
    async def get_session(cls):
        """Get a database session."""
        if cls.engine is None:
            raise Exception("Database not initialized")
        
        async_session = sessionmaker(
            cls.engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()

# Keep the get_db function for compatibility
async def get_db():
    """
    Get database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()