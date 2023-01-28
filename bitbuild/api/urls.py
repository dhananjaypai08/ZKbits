from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title=  'Inventory API')

urlpatterns = [
    path('docs/', schema_view),
    path('', views.api, name='apihome'),
    path('view/', views.view, name='view'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('add/', views.add, name='add'),
]
