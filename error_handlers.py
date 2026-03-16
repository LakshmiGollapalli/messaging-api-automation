from flask import jsonify
from utils.logger import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.error("Unhandled exception", error=str(error))

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500
