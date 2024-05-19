#!/bin/bash

PROJECT_NAME=pamps

# Arquivos na raiz
touch setup.py
touch {settings,.secrets}.toml
touch {requirements,MANIFEST}.in
echo "graft ${PROJECT_NAME}" > MANIFEST.in
touch Dockerfile.dev docker-compose.yaml

# Imagem do banco de dados
mkdir postgres
touch postgres/{Dockerfile,create-databases.sh}

# Aplicação
mkdir -p ${PROJECT_NAME}/{models,routes}
touch ${PROJECT_NAME}/default.toml
touch ${PROJECT_NAME}/{__init__,cli,app,auth,db,security,config}.py
touch ${PROJECT_NAME}/models/{__init__,post,user}.py
touch ${PROJECT_NAME}/routes/{__init__,auth,post,user}.py

# Testes
touch test.sh
mkdir tests
touch tests/{__init__,conftest,test_api}.py