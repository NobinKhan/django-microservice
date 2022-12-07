from django_socio_grpc import proto_serializers
import quickstart.grpc.quickstart_pb2 as quickstart_pb2
from .models import Question


class QuestionProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]