#!/usr/bin/env bash

echo "Dropando database Dwdufry..."
docker exec -it mysql_dufry mysql -u root -p986124 -e "DROP DATABASE IF EXISTS Dwdufry;"

echo "Criando database Dwdufry..."
docker exec -it mysql_dufry mysql -u root -p986124 -e "CREATE DATABASE Dwdufry;"

echo "Rodando dump..."
docker exec -i mysql_dufry mysql -u root -p986124 Dwdufry < dump.sql

echo "Finalizado."