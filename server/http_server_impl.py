import json
import http.server
import socketserver
import threading
import requests  # For sending HTTP POST requests
from message import Message
from server.base_server import BaseServer


class HTTPServerImpl(BaseServer):

    def __init__(self, host, port, peer_host=None, peer_port=None):
        super().__init__(host, port, peer_host, peer_port)

        # Custom HTTP server to hold a reference to the parent BaseServer
        class CustomHTTPServer(socketserver.TCPServer):
            def __init__(self, server_address, RequestHandlerClass, base_server):
                super().__init__(server_address, RequestHandlerClass)
                self.base_server = base_server

        # Custom RequestHandler that interacts with BaseServer
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    message = json.loads(post_data.decode('utf-8').rstrip())
                    # Access BaseServer through CustomHTTPServer
                    self.server.base_server.received_messages.put(Message(**message))
                    self.send_response(200)
                    self.end_headers()
                except Exception as e:
                    self.send_error(500, f"Error receiving message: {e}")

        # Use the custom HTTP server to include a reference to the parent
        self.httpd = CustomHTTPServer((self.host, self.port), RequestHandler, self)

    def start_server(self):
        """Starts the server to listen for incoming connections."""
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.start()
        self.print(f'Server started and listening at {self.host}:{self.port}')

    async def send_to_outbox(self, message: Message):
        message_str = json.dumps(message.__dict__)
        self.sent_messages.put(message_str)
        self.print(f"Saved message to outbox queue: {message_str}")

    async def flush_outbox(self):
        """Sends all messages in the outbox to the peer."""
        try:
            while not self.sent_messages.empty():
                message = self.sent_messages.get()
                if self.peer_host and self.peer_port:
                    url = f"http://{self.peer_host}:{self.peer_port}"
                    response = requests.post(url, json=json.loads(message))
                    if response.status_code == 200:
                        self.print(f"Sent message to agent from outbox queue: {message}")
                    else:
                        self.print(f"Failed to send message: {message.__dict__}, error code: {response.status_code}")
        except Exception as e:
            self.print(f"Failed to establish connection with server")
            self.is_connected = False

    async def run(self):
        """Starts the server and attempts to connect to the peer."""
        self.start_server()
