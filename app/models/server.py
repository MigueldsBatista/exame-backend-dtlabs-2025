from models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Server(Base):
    __tablename__ = 'server'

    id = Column(String(26), primary_key=True)  # ULID
    server_name = Column(String(255), nullable=False, unique=True)
    created_by = Column(Integer(), ForeignKey('user.id'), nullable=False)
    
