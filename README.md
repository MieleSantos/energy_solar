# Energy - Solar Plant Manager

Aplicação Flask para gestão de usinas solares com frontend simples, API REST, banco relacional e infraestrutura para Docker/Kubernetes.

## Stack

- Python 3.12
- Flask + Flask-SQLAlchemy + Marshmallow
- Flask-Migrate (Alembic)
- PostgreSQL (produção/containers) e SQLite (desenvolvimento)
- Pytest + Ruff
- Docker/Compose + Kubernetes manifests

## Configuração de ambiente

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
2. Atualize os valores de `.env` com credenciais reais para seu ambiente.

## Execução com Docker Compose

```bash
docker compose up -d --build
```

Aplicação: `http://localhost:5000`

## Execução local com Poetry

```bash
poetry install
cp .env.example .env
poetry run flask --app run.py db upgrade
poetry run python run.py
```

Aplicação: `http://localhost:5000`

## Kubernetes (Minikube)

1. Atualize `k8s/secret.yaml` com credenciais seguras antes de aplicar.
2. Suba os manifests:
   ```bash
   kubectl apply -f k8s/
   ```

## Migrations

Comandos úteis:

```bash
poetry run flask --app run.py db upgrade
poetry run flask --app run.py db migrate -m "describe change"
```

## Qualidade

```bash
poetry run ruff check .
PYTHONPATH=. poetry run pytest
```

Há pipeline em `.github/workflows/ci.yml` executando lint e testes em `push` e `pull_request`.

