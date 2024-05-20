# FastAPI

- Woskshop repo: 
https://github.com/rochacbruno/fastapi-workshop

```
#python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt # apenas ambiente dev

#chmod +x create-project-files.sh 
#./create-project-files.sh
https://github.com/rochacbruno/fastapi-project-template

pip-compile requirements.in # gera requirements.txt para prod (com versões), para build determinístico
pip install -e . # instala o requirements.txt e o projeto permitindo ir editando o projeto sem reinstala-lo

vscode: ctrl+shift+p - python select interpreter...

docker build -f Dockerfile.dev -t pamps:latest .
docker run --rm -it -v $(pwd):/home/app/api -p 8000:8000 pamps
docker compose up -d #--build
docker compose logs -f
http://localhost:8000/docs
docker compose exec api bash
pamps --help

alembic init migrations
edit migrations/env.py
edit migrations/script.py.mako
docker compose exec api bash
alembic revision --autogenerate -m "Initial"
alembic upgrade head


```