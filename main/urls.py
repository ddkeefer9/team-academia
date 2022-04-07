from django.urls import path
from main.views import basic_views, reports_view, smart_view, historical_view, degree_comparison_view
urlpatterns = [
    path("", basic_views.HomePage.display_index, name="home"),
    path("smart_assistant", smart_view.SmartAssistantPage.display_smartAssistant, name="smartAssistant"),
    path("pdfGen", reports_view.PDFPage.display_pdfGen, name="pdfGen"),
    path("pdfDegreeGen", reports_view.PDFPage.display_degree_pdfGen, name="pdfDegreeGen"),
    path("degreeDropdown", basic_views.HomePage.display_sendDegrees, name="degreeDropdown"),
    path("degree_comparison", degree_comparison_view.DegreeCompPage.display_degree_comp, name="degreecomparison"),
    path("historical", historical_view.HistoricalPage.display_historical, name="historical"),
    path("assistant", basic_views.HomePage.page_traversal, name="traverse")
]