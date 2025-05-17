from django.urls import path
from .views import CandidateCreateView, CandidateDetailView


urlpatterns = [
    path("candidate", CandidateCreateView.as_view(), name="candidature-create"),
    path("candidate/<uuid:pk>", CandidateDetailView.as_view(), name="candidate-detail"),
]
