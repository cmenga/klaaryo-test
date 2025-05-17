from candidate.grpc import candidate_pb2_grpc
from candidate.grpc.candidate_service import CandidateStatusService


def grpc_handlers(server):
    candidate_pb2_grpc.add_CandidateStatusServiceServicer_to_server(
        CandidateStatusService.as_servicer(), server
    )
