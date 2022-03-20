from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("smartAssistant", views.smartAssistant, name="smartAssistant"),
    path("pdfGen", views.pdfGen, name="pdfGen")
    path("degreeDropdown", views.sendDegrees, name="degreeDropdown")
]