 Prácticas de Python e Ingeniería de Datos con AWS

Descripción del proyecto

Este repositorio contiene cinco prácticas desarrolladas en Python, enfocadas en la generación, limpieza, transformación y organización de datos, así como en la implementación de un proceso ETL utilizando PostgreSQL y Amazon S3.

Cada práctica aborda diferentes conceptos de ingeniería de datos y permite desarrollar habilidades para trabajar con información, preparar conjuntos de datos y almacenarlos para su posterior análisis.

Práctica 1. Generación de transacciones

Archivo: generar_transacciones.py

Esta práctica consiste en generar datos de transacciones utilizando Python para crear registros que puedan utilizarse en pruebas y análisis de información.

Objetivos:
- Generar registros de transacciones.
- Crear datos para realizar pruebas.
- Organizar información para su procesamiento.
- Preparar datos para prácticas posteriores.

Tecnologías utilizadas:
- Python
- Bibliotecas de generación y manipulación de datos utilizadas en el script.

Práctica 2. Construcción de una tabla de hechos

Archivo: fact_table.py

Esta práctica se enfoca en la construcción de una tabla de hechos, una estructura utilizada en el modelado dimensional para organizar información destinada al análisis de datos.

Objetivos:
- Organizar información en una estructura analítica.
- Identificar medidas y datos relevantes.
- Preparar información para consultas y análisis.
- Aplicar conceptos básicos de modelado de datos.

Tecnologías utilizadas:
- Python
- Pandas y NumPy, si están incluidos en la implementación.

Práctica 3. Limpieza y preparación de datos

Archivo: limpiez.py

Esta práctica aborda la limpieza y preparación de datos para mejorar su calidad antes de realizar análisis o procesamiento adicional.

Objetivos:
- Identificar valores faltantes.
- Detectar posibles valores atípicos.
- Aplicar técnicas de limpieza de datos.
- Preparar conjuntos de datos para su análisis.
- Mejorar la calidad y consistencia de la información.

Tecnologías utilizadas:
- Python
- Pandas
- NumPy
- Scikit-learn, si se utiliza en el código.

Práctica 4. Generación de datos estratificados

Archivo: generar_datos_estratificados.py

Esta práctica se centra en la generación de datos sintéticos y en la preparación de conjuntos de datos mediante técnicas de estratificación. Estos procedimientos ayudan a crear datos de prueba y a mantener una distribución representativa de las categorías de una variable.

Objetivos:
- Generar datos sintéticos.
- Organizar variables para su análisis.
- Aplicar técnicas de división estratificada.
- Preparar conjuntos de datos para experimentos de aprendizaje automático.
- Facilitar las pruebas de modelos y algoritmos.

Tecnologías utilizadas:
- Python
- Faker
- Pandas
- NumPy
- Scikit-learn, si se utiliza en el código.

Práctica 5. Pipeline ETL automatizado con PostgreSQL y AWS S3

Archivo principal: etl_pipeline.py

Esta práctica implementa un proceso ETL (*Extract, Transform, Load*) utilizando Python para extraer datos transaccionales desde PostgreSQL, transformarlos y cargar el resultado en un bucket de Amazon S3 en formato Apache Parquet.

Fases del proceso ETL

1. Extracción (Extract)

Se establece una conexión con PostgreSQL para consultar los datos que se utilizarán durante el proceso.

2. Transformación (Transform)

Se procesan los datos mediante técnicas de transformación, como la normalización Min-Max, la discretización de edades y la creación de características para el análisis.

3. Carga (Load)

Los datos procesados se convierten al formato Apache Parquet y se cargan en un bucket de Amazon S3 para su almacenamiento.

Arquitectura

PostgreSQL → ETL con Python → Transformación de datos → Apache Parquet → Amazon S3

Objetivos
- Conectar Python con PostgreSQL.
- Extraer información mediante consultas SQL.
- Transformar y normalizar los datos.
- Crear variables derivadas para el análisis.
- Exportar los resultados en formato Parquet.
- Automatizar la carga de datos a Amazon S3.

Tecnologías utilizadas:
- Python
- PostgreSQL
- SQLAlchemy
- Pandas
- Scikit-learn
- Boto3
- PyArrow
- Amazon S3
