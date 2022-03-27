from django.urls import path
from . import views

urlpatterns = [
    path('getAddressDetails/',views.getAddressDetails,name="address-details"),
    
]