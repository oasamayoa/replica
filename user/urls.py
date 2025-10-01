from django.urls import path
from user.views import ListPostgres, ListMysql, ListBitacora

urlpatterns = [
    path('data-postgres/', ListPostgres.as_view(), name='data_postgres'),
    path('data-mysql/', ListMysql.as_view(), name='data_mysql'),
    path('bitacora/', ListBitacora.as_view(), name='bitacora_list')
]