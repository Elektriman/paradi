import os
from flask import Flask, abort, request, make_response
import json

LWD = os.path.dirname(os.path.abspath(__name__))
with open("http.json", "r") as f:
    http_dict = json.load(f)


def create_app(config: dict = None):
    app_instance = Flask(__name__)
    app_instance.config.from_object(config)
    return app_instance


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


app = create_app()


@app.route("/")
def index():
    return make_response(http_dict["200"], 200)


@app.route("/http/<int:status_code>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def http_code_check(status_code: int):
    if status_code >= 400:
        abort(status_code)

    return make_response(http_dict[str(status_code)], status_code)


@app.route("/post/<string:input_type>", methods=["POST"])
def post(input_type: str):
    response = make_response(f"{input_type} post successfully", 200)
    response.content_type = "application/json"

    match input_type:
        case "data":
            response.data = request.data
        case "args":
            response.data = json.dumps(request.args)
        case "form":
            response.data = json.dumps(request.form)
        case "files":
            files_submitted = {filename: file.content_length for filename, file in request.files.items()}
            response.data = json.dumps(files_submitted)
        case "values":
            data_submitted = {"args": request.args,
                              "form": request.form}
            response.data = json.dumps(data_submitted)
        case "json":
            response.data = request.json
        case _:
            abort(400)

    return response


@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
