from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("network/", include("network.urls", namespace="network")),
    path("api-auth/", include("rest_framework.urls")),  #для авторизации через браузер

]
