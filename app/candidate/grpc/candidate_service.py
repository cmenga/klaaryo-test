from django_grpc_framework import generics
from core.models import Candidate
from candidate.grpc import candidate_pb2
from candidate.serializers import CandidateStatusResponseSerializer


class CandidateStatusService(generics.ModelService):
    queryset = Candidate.objects.all()
    serializer_class = CandidateStatusResponseSerializer

    def GetCandidateStatus(self, request, context):
        try:
            candidate = self.queryset.get(id=request.id)
            serializer = self.serializer_class(candidate)
            return serializer.to_proto()
        except Candidate.DoesNotExist:
            context.set_code(5)  # NOT_FOUND
            context.set_details("Candidate not found")
            return candidate_pb2.CandidateStatusResponse()
