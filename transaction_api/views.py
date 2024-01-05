from datetime import date
import os
from celery.result import AsyncResult
from django.http import HttpResponse, FileResponse
import pkg_resources
from rest_framework import generics
from rest_framework.decorators import api_view

from transaction_api.utils import secret_id

from .models import Transaction
from transaction_api.serializer import TransactionSerializer
from rest_framework.response import Response
from navya_project.tasks import generate_pdf_task
from django.conf import settings


def packages_list(request):
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(
        ["%s==%s" % (i.key, i.version) for i in installed_packages]
    )
    html_output = "<h1>All Installed packages </h1><br>"

    for package in installed_packages_list:
        html_output += f"<li>{package}</li></br>"

    return HttpResponse(html_output)


class CreateGetTransactions(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetOneTransaction(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "transaction_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance,
        )
        return Response(serializer.data, status=200)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


@api_view(["GET"])
def generate_pdf_view(request):
    transactions_data = []
    query = Transaction.objects.all()
    for data in query:
        transactions_data.append(
            {
                "id": data.transaction_id,
                "date": data.transaction_date.date(),
                "phone": data.user_info.phone,
                "email": data.user_info.email,
                "amount": data.amount,
                "name": data.user_info.name,
            }
        )
    time = date.today()
    filename = f"{time}-transaction_report-{secret_id(3)}.pdf"
    header = ["Transaction ID", "Name", "Phone", "Email", "Amount", "Transaction Date"]
    generate_pdf_task.delay(filename, transactions_data, header)

    download_link = request.build_absolute_uri("/") + "api/v1/download/" + filename
    return Response(
        {
            "message": "PDF generation in progress. Download link:",
            "download_link": download_link,
        }
    )


@api_view(["GET"])
def generate_pdf_by_transaction_id_view(request, transaction_id):
    query = Transaction.objects.all().filter(transaction_id=transaction_id).first()
    if not query:
        return Response({"error": "No data Found !!"}, status=400)
    header = ["Transaction ID ", query.transaction_id]
    transactions_data = [
        {"name": "Name", "data": query.user_info.name},
        {"phone": "Phone", "data": query.user_info.phone},
        {"Email": "Email", "data": query.user_info.email},
        {"Amount": "Amount", "data": query.amount},
        {"Transaction Date": "Transaction Date", "data": query.transaction_date.date()},
    ]
    time = date.today()
    filename = f"{time}-transaction_report-{secret_id(3)}.pdf"
    generate_pdf_task.delay(filename, transactions_data, header)
    download_link = request.build_absolute_uri("/") + "api/v1/download/" + filename
    return Response(
        {
            "message": "PDF generation in progress. Download link:",
            "download_link": download_link,
        }
    )


@api_view(["GET"])
def download_pdf_view(request, filename):
    path = os.path.join(settings.BASE_DIR, "transaction_files")
    file_path = f"{path}/{filename}"
    try:
        with open(file_path, "rb") as file:
            response = HttpResponse(file.read(), content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
    except FileNotFoundError:
        return Response(
            {
                "error": "File is not found. Please ensure that the file is prepared. Also, check Celery configuration and verify your Redis setup."
            },
            status=404,
        )
