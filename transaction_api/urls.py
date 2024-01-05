from django.urls import path
from . import views

urlpatterns = [
    path(
        "transactions/", views.CreateGetTransactions.as_view(), name="transactions_api"
    ),
    path(
        "transactions/<str:transaction_id>/",
        views.GetOneTransaction.as_view(),
        name="transactions_one_api",
    ),
    path("pdf/transactions/", views.generate_pdf_view, name="generate_pdf"),
    path(
        "pdf/transactions/<str:transaction_id>/",
        views.generate_pdf_by_transaction_id_view,
        name="generate_pdf_by_id",
    ),
    path("download/<str:filename>/", views.download_pdf_view, name="download-pdf"),
]
