import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from wilder import get_mgmt_json

hostName = "localhost"
serverPort = 8080


class WildServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(get_mgmt_json(), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), WildServer)
    print("Server started http://{}:{}".format(hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
