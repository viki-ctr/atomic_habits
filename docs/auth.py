from drf_yasg import openapi

token_obtain_schema = {
    "operation_description": "Получение JWT токена",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    "responses": {
        200: openapi.Response(
            description="Успешная аутентификация",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: "Неверные учетные данные"
    }
}
