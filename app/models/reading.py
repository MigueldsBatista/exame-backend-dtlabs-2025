from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime, Float, ForeignKey
from models.base_model import Base
from sqlalchemy.orm import relationship

class Reading(Base):
    __tablename__ = 'reading'

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_ulid = Column(String(26), ForeignKey('server.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False,)
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

    
    __table_args__ = (
        CheckConstraint(
            """
            (humidity IS NOT NULL AND humidity > 0 AND humidity <= 100) OR
            (temperature IS NOT NULL) OR
            (voltage IS NOT NULL AND voltage >= 0) OR
            (current IS NOT NULL AND current >= 0)
            """,
            name='has_any_reading'
        ),
    )

    def __str__(self):
        return f"""
        Reading(server_ulid={self.server_ulid},\n
        timestamp={self.timestamp},\n
        temperature={self.temperature},\n
        humidity={self.humidity},\n
        voltage={self.voltage},\n
        current={self.current})\n
        """