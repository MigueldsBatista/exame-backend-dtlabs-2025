from typing import List
from sqlalchemy import func
from core.enums import AggregationType
from schemas.reading_schema import GetReadingParams
from repository.base_repository import BaseRepository
from models.reading import Reading
from sqlalchemy.orm import Session

class ReadingRepository(BaseRepository[Reading]):

    def __init__(self, session: Session):
        super().__init__(Reading, session)
        self.is_sqlite = 'sqlite' in str(session.bind.dialect).lower()

    def find_by_server_ulid(self, server_ulid: str):
        return self.db.query(Reading).filter(Reading.server_ulid == server_ulid).all()
    
    def find_by_criteria(self, criteria: GetReadingParams) -> List[Reading]:
        query = self.db.query(Reading)
        
        if criteria.server_ulid:
            query = query.filter(Reading.server_ulid == criteria.server_ulid)
        
        if criteria.start_time:
            query = query.filter(Reading.timestamp >= criteria.start_time)
            
        if criteria.end_time:
            query = query.filter(Reading.timestamp <= criteria.end_time)
        
        # Execute query and return domain entities
        return query.all()
    
    
    def _build_date_trunc_expr(self, aggregation_str, timestamp_column):
        """Create database-specific date truncation expression"""
        if self.is_sqlite:
            # SQLite implementation - use string operations and substr for testing
            if aggregation_str == 'day':
                # Format: YYYY-MM-DD
                return func.substr(func.datetime(timestamp_column), 1, 10)
            elif aggregation_str == 'hour':
                # Format: YYYY-MM-DD HH:00:00
                # The :00:00 is added to ensure a valid datetime format
                return func.substr(func.datetime(timestamp_column), 1, 13) + ":00:00"
            elif aggregation_str == 'minute':
                # Format: YYYY-MM-DD HH:MM:00
                return func.substr(func.datetime(timestamp_column), 1, 16) + ":00"
            else:
                # Default to just returning the timestamp
                return timestamp_column
        else:
            # PostgreSQL implementation - use date_trunc
            return func.date_trunc(aggregation_str, timestamp_column)

    def find_aggregated_readings(self, filters: GetReadingParams):
        query = self.db.query(Reading)

        aggregation_str = filters.aggregation.value if isinstance(filters.aggregation, AggregationType) else str(filters.aggregation)
        
        # Create the appropriate timestamp truncation expression based on DB type
        trunc_expr = self._build_date_trunc_expr(aggregation_str, Reading.timestamp)
        
        # Define aggregation columns
        aggregation_columns = [
            func.avg(Reading.temperature).label('temperature'),
            func.avg(Reading.humidity).label('humidity'),
            func.avg(Reading.current).label('current'),
            func.avg(Reading.voltage).label('voltage'),
        ]
        
        # Add the truncated timestamp column
        query = query.with_entities(
            trunc_expr.label('timestamp'),
            *aggregation_columns
        ).group_by(trunc_expr)


        if filters.server_ulid:
            query = query.filter(Reading.server_ulid == filters.server_ulid)

        if filters.start_time:
            query = query.filter(Reading.timestamp >= filters.start_time)

        if filters.end_time:
            query = query.filter(Reading.timestamp <= filters.end_time)

        return query.all()
