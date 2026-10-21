Práctica 5: Pipeline ETL Automatizado a AWS S3 / PostgreSQL
Este proyecto implementa un pipeline ETL (Extract, Transform, Load) en Python para extraer datos transaccionales desde una base de datos PostgreSQL local, aplicar normalización Min-Max, discretización por edades y feature engineering, y cargar el resultado procesado en formato Apache Parquet a un bucket de AWS S3.

Arquitectura
[ PostgreSQL Local ] ---> [ ETL Python ] ---> [ AWS S3 (Parquet) ]

Archivos
etl_pipeline.py: Script principal de la ETL.
requirements.txt: Librerías del entorno.
.gitignore: Exclusión de credenciales y entornos virtuales.
