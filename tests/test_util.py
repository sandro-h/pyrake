import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


def run_with_http_server(func, response):
    (server, thread) = __start_server(15150, response)
    try:
        time.sleep(0.1)
        func('http://localhost:15150')
    finally:
        server.shutdown()
        thread.join()


def __start_server(port, response):
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):  # pylint: disable=invalid-name
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())

    httpd = HTTPServer(('', port), RequestHandler)
    daemon = threading.Thread(name='daemon_server',
                              target=__run_server,
                              args=[httpd])
    daemon.setDaemon(True)
    daemon.start()
    return (httpd, daemon)


def __run_server(httpd):
    httpd.serve_forever()
