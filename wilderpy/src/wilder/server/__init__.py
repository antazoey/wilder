from flask import Flask
from flask import jsonify
from flask import request
from wilder import get_mgmt
from wilder import get_mgmt_json
from wilder.server.error import MissingAlbumError, WildServerFailureError
from wilder.server.error import MissingArtistError
from wilder.server.error import WildServerError
from wilder.server.logger import get_error_file_logger


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_unknown_errors(err):
    response = jsonify(WildServerFailureError(str(err)).dict)
    return _set_response_from_wild_error(response, err)


@app.errorhandler(WildServerError)
def handle_server_errors(err):
    response = jsonify(err.dict())
    return _set_response_from_wild_error(response, err)


def _set_response_from_wild_error(response, err):
    response.status_code = err.status_code
    return response


@app.route("/")
def mgmt():
    return get_mgmt_json(as_dict=False)


@app.route("/sign", methods=["POST"])
def sign():
    if request.method == "POST":
        data = request.form
        _verify_sign_request_data(data)
        _mgmt = get_mgmt()
        _mgmt.start_new_album(data["artist"], data["album"])
        return {"status": "successful"}


def _verify_sign_request_data(data):
    if not data.get("artist"):
        raise MissingArtistError()
    if not data.get("albums"):
        raise MissingAlbumError()
