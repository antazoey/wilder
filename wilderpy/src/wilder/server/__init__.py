from flask import Flask

from wilder import get_mgmt_json
from wilder.server.logger import get_error_file_logger


app = Flask(__name__)


@app.route('/')
def mgmt():
    return get_mgmt_json(as_dict=False)
