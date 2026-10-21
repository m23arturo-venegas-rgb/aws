import io
import boto3
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine

# --- Configuración de PostgreSQL Local ---
# --- Configuración de PostgreSQL Local ---
DB_USER = "postgres"       # O el usuario que creaste
DB_PASSWORD = "admin123" # Si usas autenticación sin contraseña localmente, deja comillas vacías ("")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "etldb"          # Cambiado a la base de datos etldb
# --- Configuración de AWS S3 ---
BUCKET_NAME = "aws-academy-datacenter-bucket-23-01-010"
S3_KEY = "processed/etl_output.parquet"

def pipeline_etl_completo():
    print("=== 1. FASE DE EXTRACCIÓN (Extract desde PostgreSQL Local) ===")
    # Crear la cadena de conexión usando SQLAlchemy
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)

    # Consulta SQL para extraer los datos
    query = "SELECT cliente, edad, monto_compras FROM clientes;"
    
    # Lectura directa desde PostgreSQL a un DataFrame de Pandas
    df_raw = pd.read_sql(query, con=engine)
    print("Datos extraídos exitosamente desde PostgreSQL:")
    print(df_raw.head())

    print("\n=== 2. FASE DE TRANSFORMACIÓN (Transform) ===")
    # Generalización
    df_raw['categoria_edad'] = pd.cut(
        df_raw['edad'], 
        bins=[0, 25, 50, 100], 
        labels=['Joven', 'Adulto', 'Senior']
    )
    
    # Normalización Min-Max de monto_compras
    scaler = MinMaxScaler()
    df_raw['monto_normalizado'] = scaler.fit_transform(df_raw[['monto_compras']])
    
    # Feature Engineering (Construcción)
    df_raw['score_promocional'] = df_raw['monto_normalizado'] * 100
    
    print("\nDataset Transformado:")
    print(df_raw)

    print("\n=== 3. FASE DE CARGA (Load a AWS S3) ===")
    # Convertir a Parquet en memoria
    buffer = io.BytesIO()
    df_raw.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)

    # Subir a S3
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=S3_KEY,
        Body=buffer.getvalue()
    )
    print(f"-> Éxito: Archivo procesado guardado en s3://{BUCKET_NAME}/{S3_KEY}")

if __name__ == "__main__":
    pipeline_etl_completo()
