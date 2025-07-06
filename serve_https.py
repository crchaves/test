import http.server
import ssl
import argparse
import os


parser = argparse.ArgumentParser(description="Simple HTTPS server")
parser.add_argument("--cert", default="cert.pem", help="SSL certificate path")
parser.add_argument("--key", default="key.pem", help="SSL private key path")
parser.add_argument("--port", type=int, default=8443, help="Port to bind")
parser.add_argument("--directory", default=".", help="Directory to serve")

args = parser.parse_args()

handler = http.server.SimpleHTTPRequestHandler

httpd = http.server.HTTPServer(("0.0.0.0", args.port), handler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    server_side=True,
    certfile=args.cert,
    keyfile=args.key,
)

print(f"Serving HTTPS on port {args.port} (directory: {args.directory})...")

os.chdir(args.directory)
httpd.serve_forever()
