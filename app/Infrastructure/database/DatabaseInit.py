from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.Domain.Base import EntityMeta

#from app.Infrastructure.Config.Enviroment import get_enviroment_variables

# Runtime Environment Configuration
#env = get_enviroment_variables()

# Generate Database URL
DATABASE_URL = f"{"mysql+asyncmy"}://{"root"}:{"longNam2403"}@{"localhost"}:{"3306"}/{"testdatabase"}"

# Create Database Engine
Engine = create_async_engine(
    DATABASE_URL, echo=True, future=True
)

async def init_models():
    async with Engine.begin() as conn:
        # await conn.run_sync(EntityMeta.metadata.drop_all)  # Uncomment nếu muốn xóa các bảng cũ
        await conn.run_sync(EntityMeta.metadata.create_all)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=Engine)

@asynccontextmanager
async def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()