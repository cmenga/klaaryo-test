from rest_framework import serializers
from core.models import Candidate

from django_grpc_framework import proto_serializers
from candidate.grpc import candidate_pb2


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        read_only_fields = ["id", "created_at", "update_at", "screening_log", "status"]


class CandidateStatusResponseSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Candidate
        proto_class = candidate_pb2.CandidateStatusResponse
        fields = ["status", "screening_log"]
