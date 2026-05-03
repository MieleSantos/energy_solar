# ☀️ Energy - Solar Plant Manager

Bem-vindo ao repositório do **Sistema de Gestão de Usinas Solares**!

O objetivo desta aplicação é fornecer um painel administrativo (Dashboard) moderno e eficiente para o monitoramento e gerenciamento de usinas solares, englobando operações completas de CRUD com foco em performance, escalabilidade e boas práticas de engenharia de software.

---

## 🛠 Tecnologias Utilizadas

O projeto foi construído utilizando um ecossistema robusto e moderno, alinhado aos requisitos da vaga:

**Backend:**
- **Python 3.12**
- **Flask** (Framework principal utilizando a arquitetura de App Factory)
- **SQLAlchemy** (ORM para abstração do banco de dados)
- **Marshmallow** (Para sanitização, validação de schemas e serialização de JSON)
- **Pytest** (Para testes automatizados de unidade e integração)
- **Ruff** (Linter e formatador garantindo conformidade com a PEP-8)
- **Poetry** (Gerenciamento profissional de pacotes e ambientes virtuais)

**Frontend:**
- **HTML5 & Vanilla JS** (Fetch API para consumo assíncrono do backend, SPA feel)
- **Vanilla CSS** (Design premium customizado com técnica de *Glassmorphism* e Dark Mode)

**Infraestrutura / DevOps:**
- **Docker & Docker Compose** (Para containerização da aplicação e do banco de dados)
- **Kubernetes (Minikube)** (Orquestração de contêineres utilizando ConfigMaps, Secrets, PVCs, Deployments e Services)
- **PostgreSQL** (Banco de dados relacional oficial de produção)

---

## 🏗 Arquitetura & Boas Práticas

Esta aplicação foi arquitetada seguindo as melhores práticas exigidas em ambientes de alta demanda:

1. **App Factory Pattern**: A inicialização do Flask e suas extensões (banco de dados, schemas) é encapsulada na função `create_app()`, permitindo múltiplos ambientes (Produção, Teste, Dev) isolados e limpos.
2. **Separação de Responsabilidades (Blueprints)**: As rotas da API estão isoladas no pacote `api/`, garantindo que o código seja fácil de manter e escalar.
3. **Data Validation**: A validação das requisições POST não ocorre no controlador. Todo payload é interceptado e validado de forma estrita pelo `Marshmallow` em `api/schemas.py`, retornando respostas amigáveis (`422 Unprocessable Entity`) em caso de violações de schema.
4. **Resiliência de Banco de Dados**: A aplicação conecta no PostgreSQL no ambiente Docker/Kubernetes, mas implementa um *fallback automático* para instâncias locais com SQLite caso seja executada diretamente na máquina, evitando que a aplicação quebre durante testes manuais rápidos.
5. **Orquestração K8s**: Toda a infraestrutura foi mapeada para manifestos nativos do Kubernetes (`k8s/`), separando a configuração de credenciais via `Secret` e variáveis globais em `ConfigMap`, e garantindo a persistência do banco com um `PersistentVolumeClaim`.

---

## 🚀 Como Executar o Projeto

Existem duas maneiras recomendadas de rodar a aplicação:

### Opção 1: Via Docker (Recomendado)
Esta opção levanta a aplicação e um container dedicado do **PostgreSQL**. É o cenário mais próximo do ambiente de produção.

1. Certifique-se de ter o [Docker Desktop](https://www.docker.com/products/docker-desktop) rodando.
2. No terminal, na raiz do projeto, execute:
   ```bash
   docker-compose up -d --build
   ```
3. A aplicação estará disponível em: [http://localhost:5000](http://localhost:5000)

### Opção 2: Localmente via Poetry (Modo Desenvolvimento)
Ideal para desenvolver e executar os testes. Os dados serão salvos num arquivo SQLite `local.db`.

1. Certifique-se de ter o [Poetry](https://python-poetry.org/) instalado.
2. Instale as dependências:
   ```bash
   poetry install
   ```
3. Inicie o servidor:
   ```bash
   poetry run python run.py
   ```
4. A aplicação estará disponível em: [http://localhost:5000](http://localhost:5000)

### Opção 3: Via Kubernetes (Minikube)
O projeto contém a definição completa de manifestos na pasta `k8s/` para rodar num cluster de Kubernetes.

1. Inicie o Minikube:
   ```bash
   minikube start
   ```
2. Configure seu terminal para construir imagens dentro do Minikube:
   ```bash
   eval $(minikube docker-env)
   # Ou no Windows PowerShell: minikube docker-env | Invoke-Expression
   ```
3. Construa a imagem da aplicação:
   ```bash
   docker build -t flask-app:latest .
   ```
4. Aplique os manifestos e aguarde os pods iniciarem:
   ```bash
   kubectl apply -f k8s/
   kubectl get pods -w
   ```
5. Faça o redirecionamento de porta para acessar a aplicação:
   ```bash
   kubectl port-forward svc/web 5000:5000
   ```
6. A aplicação estará disponível em: [http://localhost:5000](http://localhost:5000) (ou utilize `minikube service web --url` caso prefira o túnel).

---

## 🧪 Testes e Qualidade de Código

A qualidade do código é fundamental. O projeto conta com uma suíte de testes garantindo que o CRUD funcione e falhe exatamente quando deve (ex: testando as validações do Marshmallow).

Para rodar a bateria de testes automatizados (`pytest`), execute:
```bash
$env:PYTHONPATH="."; poetry run pytest
```
*(No Linux/Mac: `PYTHONPATH=. poetry run pytest`)*

Para rodar a verificação de sintaxe e padrões de projeto (PEP-8) usando o `Ruff`:
```bash
poetry run ruff check .
```

---

## ✨ Features Implementadas
- **Dashboard em Tempo Real**: Visualize a quantidade de usinas ativas e a capacidade total gerada.
- **Cadastro de Usinas**: Adicione o Nome, Localização, Status e Capacidade (kW).
- **Tratamento de Erros Moderno**: Tentativas de inserir usinas com capacidades inválidas ou sem nome disparam mensagens de erro validadas.
- **Deleção Segura**: Exclusão de registros com interface responsiva e feedback imediato.

