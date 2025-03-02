from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from models.base_model import Base

class Reading(Base):
    __tablename__ = 'reading'

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_ulid = Column(String(26), ForeignKey('server.id'), nullable=False)
    timestamp_ms = Column(DateTime, nullable=False,)
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

    def __str__(self):
        return f"""
        Reading(server_ulid={self.server_ulid},\n
        timestamp={self.timestamp},\n
        temperature={self.temperature},\n
        humidity={self.humidity},\n
        oltage={self.voltage},\n
        current={self.current})\n
        """