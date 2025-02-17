from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#from app.Infrastructure.Config.Enviroment import get_enviroment_variables

# Runtime Environment Configuration
#env = get_enviroment_variables()

# Generate Database URL
DATABASE_URL = f"{"mysql+mysqlconnector"}://{"root"}:{"longNam2403"}@{"localhost"}:{"3306"}/{"testdatabase"}"

# Create Database Engine
Engine = create_engine(
    DATABASE_URL, echo=True, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()