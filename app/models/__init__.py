from models.base_model import Base
from models.user import User
from models.server import Server
from models.reading import Reading

# List all models here to ensure they're imported before Base.metadata is used
__all__ = ['User', 'Server', 'Reading']
