from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_env_variable(var_name, default=None):
    """
    Obtém uma variável de ambiente ou retorna o valor padrão.
    Se não houver valor padrão e a variável não existir, lança uma exceção.
    """
    value = os.getenv(var_name)
    if value is None:
        if default is None:
            raise ValueError(f"Environment variable {var_name} not found")
        return default
    return value

# Configurações do JWT
SECRET_KEY = get_env_variable("SECRET_KEY", "your-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Configurações do banco de dados

DB_USER = get_env_variable("DB_USER")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
DB_NAME = get_env_variable("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

