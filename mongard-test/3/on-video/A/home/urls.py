from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('' , views.HomeView.as_view() , name='home'),
    path('detail/<slug:product_slug>' , views.ProductDetailView.as_view() , name='product_detail')
]