from wilder.config import create_config_obj
from wilder.client.connection import create_connection, Connection


def create_client(config_file_path):
    config = create_config_obj(config_file_path)
    conn = Connection(config.host, config.port)
    return WildClient(conn)


class WildClient:
    def __init__(self, connection=None):
        self.connection = connection or create_connection("127.0.0.1", 443)

    def get_artists(self):
        return self.connection.get("/artists")
