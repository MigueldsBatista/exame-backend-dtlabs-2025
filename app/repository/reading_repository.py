from sqlalchemy import func
from core.enums import AggregationType
from schemas.reading_schema import GetReading
from repository.base_repository import BaseRepository
from models.reading import Reading
from sqlalchemy.orm import Session

class ReadingRepository(BaseRepository[Reading]):
    """Repository for Reading model
    This repository handles the database operations for the Reading model."""

    def __init__(self, session: Session):
        """Initialize the repository with a database session."""
        super().__init__(Reading, session)

    def find_by_server_ulid(self, server_ulid: str):
        """Find readings by server ULID.
        
        Args:
            server_ulid (str): The unique identifier of the server.
        
        Returns:
            List[Reading]: A list of readings associated with the given server ULID.
        """
        return self.db.query(Reading).filter(Reading.server_ulid == server_ulid).all()


    def find_by_filters(self, filters: GetReading=None):
        """Find readings by query parameters.
        
        Args:
            filters (GetReading): The query parameters.
        
        Returns:
            List[Reading]: A list of readings that match the query parameters.
        """

        query = self.db.query(Reading)

        if not filters:
            return self.find_all()

        if filters.server_ulid:
            query = query.filter(Reading.server_ulid == filters.server_ulid)

        if filters.start_time:
            query = query.filter(Reading.timestamp_ms >= filters.start_time)

        if filters.end_time:
            query = query.filter(Reading.timestamp_ms <= filters.end_time)

        aggregation_columns = [
            func.avg(Reading.temperature).label('temperature'),
            func.avg(Reading.humidity).label('humidity'),
            func.avg(Reading.current).label('current'),
            func.avg(Reading.voltage).label('voltage'),
        ]

        if filters.aggregation:
            aggregation_str = filters.aggregation.value if isinstance(filters.aggregation, AggregationType) else str(filters.aggregation)

            query = query.with_entities(
                func.date_trunc(aggregation_str, Reading.timestamp_ms).label('timestamp'),
                *aggregation_columns
            ).group_by(func.date_trunc(aggregation_str, Reading.timestamp_ms))

        return query.all()
        