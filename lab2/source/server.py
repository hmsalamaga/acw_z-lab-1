#!/usr/bin/env python3
import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs
import time

#print('source code for "http.server":', http.server.__file__)

os.environ['TZ'] = 'Europe/Warsaw'
time.tzset()

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):

        print(self.path)
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            query_params = parse_qs(parsed_path.query)

            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()

            if query_params['cmd'] == ['rev']:
                reversed_strgs = [strg[::-1] for strg in query_params['str']]
                self.wfile.write(str.encode(f'{reversed_strgs}\n'))
            elif query_params['cmd'] == ['time']:
                self.wfile.write(str.encode(f'{time.strftime("%H:%M:%S")}\n'))
            else:
                self.wfile.write(b"Hello World!\n")
            
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
