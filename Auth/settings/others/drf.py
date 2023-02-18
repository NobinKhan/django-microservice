# Django Rest Framework
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "apps.api.exception_handlers.drf_default_with_modifications_exception_handler",
    # 'EXCEPTION_HANDLER': 'styleguide_example.api.exception_handlers.hacksoft_proposed_exception_handler',
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": [],
}
