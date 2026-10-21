import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Nombre del bucket S3
BUCKET_NAME = "aws-academy-datacenter-bucket-23-01-010"

# Región de AWS Academy
REGION = "us-west-2"


def listar_bucket():
    try:
        # Conexión con Amazon S3
        s3 = boto3.client(
            "s3",
            region_name=REGION
        )

        print("=" * 60)
        print("CONTENIDO DEL BUCKET S3")
        print("=" * 60)
        print(f"Bucket: {BUCKET_NAME}")
        print()

        # Paginador para obtener todos los objetos
        paginator = s3.get_paginator("list_objects_v2")

        contador = 0

        for pagina in paginator.paginate(Bucket=BUCKET_NAME):

            objetos = pagina.get("Contents", [])

            for objeto in objetos:
                contador += 1

                print(f"{contador}. {objeto['Key']}")
                print(f"   Tamaño: {objeto['Size']} bytes")
                print(f"   Última modificación: {objeto['LastModified']}")
                print("-" * 60)

        print()
        print("=" * 60)
        print(f"TOTAL DE OBJETOS: {contador}")
        print("=" * 60)

    except NoCredentialsError:
        print("ERROR: No se encontraron las credenciales de AWS.")

    except ClientError as e:
        print("ERROR DE AWS:")
        print(e)

    except Exception as e:
        print("ERROR:")
        print(e)


if __name__ == "__main__":
    listar_bucket()