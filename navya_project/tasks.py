# tasks.py

from celery import shared_task

from django.conf import settings

from transaction_api.generate_pdf import generate_transaction_pdf
import os


@shared_task()
def dump_transaction_files(bind=True):
    folder_path = os.path.join(settings.BASE_DIR, "transaction_files")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if filename.endswith(".pdf") and (
                os.path.isfile(file_path) or os.path.islink(file_path)
            ):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


@shared_task
def generate_pdf_task(filename, table_list: list, header=None):
    generate_transaction_pdf(filename, table_list, header)
