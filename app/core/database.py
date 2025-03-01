from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para usar em rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
