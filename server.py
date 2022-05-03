import json
from urllib.parse import parse_qs
from tickets_db import Tickets
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
import random

class MyRequestHandler( BaseHTTPRequestHandler ):

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def load_session(self):
        self.load_cookie()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
        self.send_header("Access-Control-Allow-Credentials","true")
        self.send_cookie()


        super().end_headers()

    def handleRetrieveTickets(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        db = Tickets()
        tickets = db.getAllTickets()
        self.wfile.write(bytes(json.dumps(tickets), "utf-8"))

    def handleCreateTicket(self):
        if "oompa" in self.cookie:
            print("oompa loompa found")
            self.handle403()
            return
        self.cookie["oompa"] = "loompa"
        self.cookie["oompa"]["samesite"] = "None"
        self.cookie["oompa"]["secure"] = True

        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        #print("raw request body: ", request_body)
        
        parsed_body = parse_qs(request_body)
        #print("parsed request body: ", parsed_body)

        ename = parsed_body['entrant_name'][0]
        #print("entrant_name: ", ename)

        eage = parsed_body['entrant_age'][0]
        #print("entrant_age: ", eage)

        gname = parsed_body['guest_name'][0]
        #print("guest_name: ", gname)

        rtoken = random.randrange(0,7)
        #print("rtoken = ", rtoken)

        db = Tickets()
        db.createTicket( ename, eage, gname, rtoken )

        self.send_response(201)
        self.send_header( "Content-Type", "application/json" )
        self.end_headers()
        self.wfile.write(bytes("Created", "utf-8"))

    def handle403(self):
        self.send_response(403)
        self.send_header( "Content-Type", "text/plain" )
        self.end_headers()
        self.wfile.write(bytes("The Oompa Loompas have already recieved your ticket. Please try again tomorrow.", "utf-8"))

    def handleNotFound(self):
        self.send_response(404)
        self.send_header( "Content-Type", "text/plain" )
        self.end_headers()
        self.wfile.write(bytes("It seems that this resource has been lost in the chocolate pipes. An Oompa Loompa will be dispacted promptly to recover the artifact.", "utf-8"))

    def do_GET(self):
        self.load_session()

        print("the request path is: ", self.path)
        parts = self.path.split( "/" )
        
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "tickets":
            self. handleRetrieveTickets()
        else:
            self.handleNotFound()


    def do_POST(self):
        self.load_session()

        if self.path == "/tickets":
            self.handleCreateTicket()

        else:
            self.handleNotFound()

class ThreadedHTTPServer( ThreadingMixIn, HTTPServer ):
    pass


def main():
    #start the server
	
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer( listen, MyRequestHandler )
    print("Listening: ", listen)
    print("The server is running")
    server.serve_forever()
    print("hello")
main()
