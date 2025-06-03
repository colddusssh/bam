from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()