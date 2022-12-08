from django_socio_grpc import proto_serializers
import grpc.account_pb2 as accPB2
from .models import Question


class QuestionProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]