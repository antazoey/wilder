from flask import Flask, jsonify
from flask import request

from wilder import get_mgmt_json
from wilder import get_mgmt
from wilder.server.error import WildServerError, MissingArtistError, MissingAlbumError
from wilder.server.logger import get_error_file_logger


app = Flask(__name__)


@app.errorhandler(WildServerError)
def handle_invalid_usage(err):
    response = jsonify(err.dict())
    response.status_code = err.status_code
    return response


@app.route('/')
def mgmt():
    return get_mgmt_json(as_dict=False)


@app.route('/sign', methods=['POST'])
def sign():
    if request.method == 'POST':
        data = request.form
        mgmt = get_mgmt()
        mgmt.start_new_album()
        

def _verify_sign_request_data(data):
    if not data.get("artist"):
        raise MissingArtistError()
    if not data.get("albums"):
        raise MissingAlbumError()
