import json

import sentry_sdk

class SentryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with sentry_sdk.start_transaction(op="http.server", name=f"{request.method} {request.path}"):
            try:
                request_info = {
                    "method": request.method,
                    "url": request.build_absolute_uri(),
                    "headers": dict(request.headers),
                    "body": request.body.decode("utf-8") if request.body else "{}"
                }

                response = self.get_response(request)

                response_info = {
                    "status_code": response.status_code,
                }

                if hasattr(response, 'content'):
                    response_info["body"] = response.content.decode("utf-8")

                sentry_sdk.capture_message(f"Запрос: {json.dumps(request_info, indent=2)}")
                sentry_sdk.capture_message(f"Ответ: {json.dumps(response_info, indent=2)}")

                return response

            except Exception as e:
                sentry_sdk.capture_exception(e)
                raise
