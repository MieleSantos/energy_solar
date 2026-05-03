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

## Deploy AWS (EC2 + RDS + ECR)

### Arquivos de produção

- `docker-compose.prod.yml`: stack de produção (somente `web`).
- `.env.prod.example`: variáveis de ambiente esperadas no servidor.
- `.github/workflows/deploy-aws-ec2.yml`: CI/CD para build, push no ECR e deploy na EC2.
- `deploy/aws/provisioning.md`: passo a passo de provisionamento AWS.
- `deploy/nginx/energy-solar.conf`: reverse proxy Nginx.

### 1) Provisionar base AWS

Siga `deploy/aws/provisioning.md` para criar:

- ECR repository
- RDS PostgreSQL privado
- EC2 com Security Groups corretos (22 restrito, 80/443 públicos, 5432 somente EC2 -> RDS)

### 2) Bootstrap da EC2

No servidor:

```bash
chmod +x deploy/aws/ec2-bootstrap.sh
./deploy/aws/ec2-bootstrap.sh
```

Crie `.env.prod` na EC2 a partir de `.env.prod.example`.

### 3) Configurar GitHub Actions deploy

No GitHub, configure:

- Environment `production`
- Secrets:
  - `AWS_DEPLOY_ROLE_ARN`
  - `EC2_SSH_PRIVATE_KEY`
- Variables:
  - `AWS_REGION`
  - `ECR_REPOSITORY`
  - `EC2_HOST`
  - `EC2_USER`
  - `APP_DIR` (ex: `/opt/energy-solar`)

O workflow de deploy executa no push para `main`.

### 4) Nginx + TLS

No servidor:

```bash
chmod +x deploy/nginx/setup_tls.sh
./deploy/nginx/setup_tls.sh your-domain.com you@example.com
```

### 5) Smoke test pós deploy

No servidor:

```bash
chmod +x deploy/aws/smoke-test.sh
./deploy/aws/smoke-test.sh https://your-domain.com
```

### 6) Rollback

Use uma tag anterior publicada no ECR:

```bash
chmod +x deploy/aws/rollback.sh
./deploy/aws/rollback.sh <previous-image-tag>
```

### Hardening recomendado

Veja `deploy/aws/hardening.md` para checklist mínimo de segurança operacional.

