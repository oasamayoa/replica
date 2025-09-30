from django.urls import path
from user.views import ListPostgres, ListMysql

urlpatterns = [
    path('data-postgres/', ListPostgres.as_view(), name='data_postgres'),
    path('data-mysql/', ListMysql.as_view(), name='data_mysql'),
]