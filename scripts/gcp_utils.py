import argparse

from google.cloud import storage
from google.cloud.exceptions import Conflict

tup_tipo_accion = ("gcs-create",)


def params():
    parser = argparse.ArgumentParser(description="Utilidades Google Cloud Platform")
    parser.add_argument("action", type=str, choices=[tup_tipo_accion[0]], help="Tipo de accion")
    parser.add_argument("bucket_name", type=str, help="Nombre del bucket", nargs="?")

    args = parser.parse_args()

    if args.action == tup_tipo_accion[0] and not args.bucket_name:
        parser.error(f"El argumento 'bucket_name' es obligatorio cuando la acción es '{tup_tipo_accion[0]}'")

    return args


def create_bucket(bucket_name):
    storage_client = storage.Client()

    try:
        bucket = storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket.name} creado exitosamente.")
    except Conflict:
        print(f"El bucket {bucket_name} ya existe.")
    except Exception as e:
        print(f"Error al crear el bucket: {e}")


def main():
    args = params()
    if args.action == tup_tipo_accion[0]:
        create_bucket(args.bucket_name)


if __name__ == "__main__":
    main()
