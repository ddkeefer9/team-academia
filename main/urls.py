from django.urls import path

from main.views import basic_views
urlpatterns = [
    path("", basic_views.index, name="home"),
    path("smartAssistant", basic_views.smartAssistant, name="smartAssistant"),
    path("pdfGen", basic_views.pdfGen, name="pdfGen"),
    path("degreeDropdown", basic_views.sendDegrees, name="degreeDropdown"),
    path("historical", basic_views.historical, name="historical")
]