import logging.config
from typing import Dict

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app, path="/metrics")

app.config['JSON_SORT_KEYS'] = False # no sorting of the output keys for jsonify
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # for pretty printing json responses

# setup the handlers and formatters
logging.config.fileConfig('logging.conf')


@app.route('/')
def home():
    app.logger.info("Home page", extra={
        "page": "home",
    })

    return jsonify({
        "page": "home"
    })


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Handler for all application exceptions
    """
    status_code = e.code if hasattr(e, 'code') else 500
    response = jsonify({"status": "error", "status_code": status_code, "error": str(e)})
    response.status_code = status_code
    app.logger.error(f"Error occurred: {str(e)}", extra={
        "type": "error",
    }, exc_info=1)

    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
