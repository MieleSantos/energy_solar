from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from api.exceptions import ApiError


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return (
            jsonify(
                {
                    "error": "Validation Error",
                    "message": "Payload validation failed",
                    "details": error.messages,
                }
            ),
            422,
        )

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return (
            jsonify(
                {
                    "error": "API Error",
                    "message": error.message,
                    "details": error.details,
                }
            ),
            error.status_code,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return (
            jsonify(
                {
                    "error": "HTTP Error",
                    "message": error.description,
                    "details": {},
                }
            ),
            error.code,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(_error):
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "details": {},
                }
            ),
            500,
        )
