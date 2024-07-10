# Descomplicando FastAPI

Criei este repo durante a realização do workshop `Criando uma API com Python e FastAPI` da [LinuxTips](https://linuxtips.io/) ([veja o meu certificado](https://www.credential.net/304de764-cfb1-49fa-8c02-9113c4245c1b)).

- Repos do instrutor do woskshop: 
    - https://github.com/rochacbruno/fastapi-workshop
    - https://github.com/rochacbruno/fastapi-project-template
- Links úteis:
    - https://fastapi.tiangolo.com/
    - https://sqlmodel.tiangolo.com/
    - https://docs.pydantic.dev/


```sh
# Algumas anotações

#python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt # apenas ambiente dev

chmod +x create-project-files.sh 
./create-project-files.sh

pip-compile requirements.in # gera requirements.txt para prod (com versões), para build determinístico
pip install -e . # instala o requirements.txt e o projeto permitindo ir editando o projeto sem reinstala-lo

vscode: ctrl+shift+p - python select interpreter...

docker build -f Dockerfile.dev -t pamps:latest .
docker run --rm -it -v $(pwd):/home/app/api -p 8000:8000 pamps
docker compose up -d #--build
docker compose logs -f
# http://localhost:8000/docs
docker compose exec api bash
pamps --help

alembic init migrations
edit migrations/env.py
edit migrations/script.py.mako
docker compose exec api bash
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```
