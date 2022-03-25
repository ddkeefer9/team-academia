from django.urls import path
from main.views import basic_views, reports_view,smart_view,historical_view
urlpatterns = [
    path("", basic_views.HomePage.display_index, name="home"),
    path("smartAssistant", smart_view.SmartAssistantPage.display_smartAssistant, name="smartAssistant"),
    path("pdfGen", reports_view.PDFPage.display_pdfGen, name="pdfGen"),
    path("degreeDropdown", basic_views.HomePage.display_sendDegrees, name="degreeDropdown"),
    path("historical", historical_view.HistoricalPage.display_historical, name="historical")
]