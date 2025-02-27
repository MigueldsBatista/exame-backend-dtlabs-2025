import os
from dotenv import load_dotenv

# Configurações

load_dotenv()

# Utilizando lazy loading para variáveis de ambiente
def get_env_variable(name, default=None):
    """Helper function to get environment variables lazily"""
    var = os.getenv(name)
    if var is None and default is not None:
        return default
    elif var is None:
        raise ValueError(f"Environment variable {name} not set")
    return var
        

# Carrega variáveis de ambiente apenas quando necessário

# Variáveis serão carregadas apenas quando acessadas
SECRET_KEY = get_env_variable("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30