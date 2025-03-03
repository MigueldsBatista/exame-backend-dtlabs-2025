# FastAPI com PostgreSQL no Docker

Este projeto é uma aplicação FastAPI conectada a um banco de dados PostgreSQL, rodando em contêineres Docker.

## Pré-requisitos

- Docker instalado ([Instalação do Docker](https://docs.docker.com/get-docker/))
- Docker Compose instalado ([Instalação do Docker Compose](https://docs.docker.com/compose/install/))

## Configuração do Ambiente

1. **Configure as variáveis de ambiente**:

   Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

   Edite o arquivo `.env` com suas configurações:
   ```properties
   # Database credentials
   DB_USER=postgres
   DB_PASSWORD=sua_senha_segura
   DB_NAME=dtlabs
   SECRET_KEY=sua_chave_secreta_muito_longa_e_segura
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ENV=Docker
   DB_HOST=db
   ```
   
   **Importante**: Substitua os valores padrão por valores seguros em ambientes de produção.

## Como Rodar o Projeto

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/MigueldsBatista/exame-backend-dtlabs-2025.git
    cd exame-backend-dtlabs-2025
    ```

2. **Construa e rode os contêineres**:
    ```bash
    docker-compose up --build
    ```

    Isso irá:
    - Construir a imagem da aplicação FastAPI
    - Iniciar o banco de dados PostgreSQL
    - Rodar a aplicação FastAPI

3. **Acesse a aplicação**:
    - FastAPI em [http://localhost:8000](http://localhost:8000)
    - Documentação interativa em [http://localhost:8000/docs](http://localhost:8000/docs)

## Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `docker-compose ps` | Verificar contêineres em execução |
| `docker-compose down` | Parar os contêineres |
| `docker-compose down -v` | Remover contêineres e volumes |
| `docker-compose logs app` | Ver logs da aplicação |
| `docker-compose logs db` | Ver logs do banco de dados |
| `docker-compose exec app bash` | Acessar o shell do contêiner da aplicação |
| `docker-compose exec db psql -U meu_usuario -d meu_banco` | Acessar o shell do banco de dados |

## Resolvendo Conflitos de Porta

Se você já tem um PostgreSQL rodando na sua máquina e ele está usando a porta 5432:

### Opção 1: Parar o PostgreSQL local

**Linux**:
```bash
sudo systemctl stop postgresql
```

**macOS** (Homebrew):
```bash
brew services stop postgresql
```

**Windows**:
Pare o serviço PostgreSQL pelo "Services Manager"

### Opção 2: Alterar a porta no docker-compose.yml

```yaml
ports:
  - "5433:5432"
```

## Verificar a conexão co o banco de dados
```bash
docker-compose exec app psql -h db -U postgres -d dtlabs
```