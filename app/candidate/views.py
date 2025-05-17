from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Candidate
from .serializers import CandidateSerializer
from .tasks import run_screening


class CandidateCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer

    def post(self, request):
        candidate = Candidate.objects.create(
            full_name=request.data.get("full_name"),
            email=request.data.get("email"),
            status="pending",
        )
        candidate.save()
        run_screening.delay(candidate.id)
        return Response(
            {
                "full_name": candidate.full_name,
                "email": candidate.email,
                "id": candidate.id,
            },
            status=HTTP_201_CREATED,
        )


class CandidateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)
