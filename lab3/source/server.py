#!/usr/bin/env python3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json

#print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def _count_chars(self, strg):
        counter = {
            "lowercase" : 0,
            "uppercase" : 0,
            "digits" : 0,
            "special" : 0
        }

        for c in strg:
            if c.isupper():
                counter["uppercase"] += 1
            elif c.islower():
                counter["lowercase"] += 1
            elif c.isdigit():
                counter["digits"] += 1
            else:
                counter["special"] += 1

        return counter
    
    def do_GET(self):

        print(self.path)
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            query_params = parse_qs(parsed_path.query)

            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=UTF-8')
            self.end_headers()
            if query_params.get('str', None):
                strg = query_params.get('str', None)[0]
                self.wfile.write(str.encode(json.dumps(self._count_chars(strg))))
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
