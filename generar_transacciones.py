import boto3
import pandas as pd
import numpy as np
import io
from botocore.exceptions import ClientError, NoCredentialsError

# ============================================================
# CONFIGURACIÓN
# ============================================================

BUCKET_NAME = "aws-academy-datacenter-bucket-23-01-010"
FILE_KEY = "raw/transacciones.csv"

# Región utilizada en AWS Academy
REGION = "us-west-2"


# ============================================================
# CONEXIÓN CON AMAZON S3
# ============================================================

s3_client = boto3.client(
    "s3",
    region_name=REGION
)


# ============================================================
# GENERAR DATOS SINTÉTICOS
# ============================================================

def generar_datos_sinteticos(cantidad=1000):

    np.random.seed(42)

    # IDs de las transacciones
    transaction_id = [
        f"TXN-{i:06d}"
        for i in range(1, cantidad + 1)
    ]

    # Fechas aleatorias
    fechas = pd.date_range(
        start="2025-01-01",
        end="2025-12-31",
        periods=cantidad
    )

    # Clientes
    customer_id = [
        f"CUST-{np.random.randint(1000, 9999)}"
        for _ in range(cantidad)
    ]

    # Productos
    productos = [
        "Laptop",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Teclado",
        "Mouse",
        "Audifonos",
        "Impresora"
    ]

    producto = np.random.choice(
        productos,
        cantidad
    )

    # Categorías
    categorias = {
        "Laptop": "Computacion",
        "Smartphone": "Telefonia",
        "Tablet": "Computacion",
        "Monitor": "Computacion",
        "Teclado": "Accesorios",
        "Mouse": "Accesorios",
        "Audifonos": "Accesorios",
        "Impresora": "Computacion"
    }

    categoria = [
        categorias[p]
        for p in producto
    ]

    # Cantidad de productos
    cantidad_productos = np.random.randint(
        1,
        6,
        cantidad
    )

    # Precio unitario
    precios = {
        "Laptop": (10000, 30000),
        "Smartphone": (5000, 25000),
        "Tablet": (3000, 15000),
        "Monitor": (2500, 10000),
        "Teclado": (300, 2000),
        "Mouse": (200, 1500),
        "Audifonos": (500, 5000),
        "Impresora": (1500, 8000)
    }

    precio_unitario = [
        round(
            np.random.uniform(
                precios[p][0],
                precios[p][1]
            ),
            2
        )
        for p in producto
    ]

    # Total de la transacción
    total = [
        round(
            cantidad_productos[i] * precio_unitario[i],
            2
        )
        for i in range(cantidad)
    ]

    # Métodos de pago
    metodos_pago = [
        "Tarjeta",
        "Transferencia",
        "PayPal",
        "Efectivo"
    ]

    metodo_pago = np.random.choice(
        metodos_pago,
        cantidad
    )

    # Estados de las transacciones
    estados = [
        "Completada",
        "Pendiente",
        "Cancelada"
    ]

    estado = np.random.choice(
        estados,
        cantidad,
        p=[0.80, 0.12, 0.08]
    )

    # Estados de envío
    estados_envio = [
        "Entregado",
        "Enviado",
        "Pendiente",
        "Cancelado"
    ]

    envio = np.random.choice(
        estados_envio,
        cantidad
    )

    # Ciudades
    ciudades = [
        "Puebla",
        "Ciudad de Mexico",
        "Tlaxcala",
        "Veracruz",
        "Oaxaca",
        "Guadalajara",
        "Monterrey",
        "Queretaro"
    ]

    ciudad = np.random.choice(
        ciudades,
        cantidad
    )

    # Crear DataFrame
    df = pd.DataFrame({
        "transaction_id": transaction_id,
        "fecha": fechas,
        "customer_id": customer_id,
        "producto": producto,
        "categoria": categoria,
        "cantidad": cantidad_productos,
        "precio_unitario": precio_unitario,
        "total": total,
        "metodo_pago": metodo_pago,
        "estado": estado,
        "estado_envio": envio,
        "ciudad": ciudad
    })

    return df


# ============================================================
# SUBIR DATASET A S3
# ============================================================

def subir_a_s3(df):

    try:

        # Convertir DataFrame a CSV en memoria
        csv_buffer = io.StringIO()

        df.to_csv(
            csv_buffer,
            index=False
        )

        # Subir directamente a S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_KEY,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )

        print()
        print("=" * 70)
        print("ARCHIVO SUBIDO CORRECTAMENTE A S3")
        print("=" * 70)
        print(f"Bucket: {BUCKET_NAME}")
        print(f"Ruta:   {FILE_KEY}")
        print(f"Filas:  {len(df)}")
        print(f"Columnas: {len(df.columns)}")
        print("=" * 70)

    except NoCredentialsError:
        print("ERROR: No se encontraron las credenciales de AWS.")

    except ClientError as e:
        print("ERROR DE AWS:")
        print(e)

    except Exception as e:
        print("ERROR:")
        print(e)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("GENERADOR DE TRANSACCIONES SINTÉTICAS")
    print("=" * 70)

    # Generar 1000 transacciones
    df_transacciones = generar_datos_sinteticos(1000)

    print()
    print("Datos sintéticos generados correctamente.")
    print()
    print("Primeras 10 transacciones:")
    print(df_transacciones.head(10))

    print()
    print("Dimensiones:")
    print(
        f"{df_transacciones.shape[0]} filas x "
        f"{df_transacciones.shape[1]} columnas"
    )

    print()
    print("Tipos de datos:")
    print(df_transacciones.dtypes)

    # Guardar localmente
    df_transacciones.to_csv(
        "transacciones.csv",
        index=False
    )

    print()
    print("Archivo local creado: transacciones.csv")

    # Subir a S3
    subir_a_s3(df_transacciones)