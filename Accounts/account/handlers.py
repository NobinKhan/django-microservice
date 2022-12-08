from django_socio_grpc.utils.servicer_register import AppHandlerRegistry
from .services import QuestionService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("account", server)
    app_registry.register(QuestionService)