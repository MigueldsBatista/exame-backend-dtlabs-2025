from models.base_model import Base
from sqlalchemy import Column, String

class Server(Base):
    __tablename__ = 'server'

    id = Column(String(26), primary_key=True)  # ULID
    server_name = Column(String(255), nullable=False)
    