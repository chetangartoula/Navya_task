# tasks.py

from celery import shared_task

from transaction_api.generate_pdf import generate_transaction_pdf


@shared_task
def generate_pdf_task(filename,table_list:list,header=None):
    generate_transaction_pdf(filename,table_list,header)
