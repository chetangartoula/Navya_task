from django.contrib import admin
from django.urls import include, path

from transaction_api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.packages_list, name="test_url"),
    path("api/v1/", include("transaction_api.urls")),
]
