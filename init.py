import RPi.GPIO as gpio
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

print("""
CS Day Wheeler V1
Coded By Yanavut Rojanapron
https://github.com/chokunplayz
""")

print("setting up GPIO MODE")

#try :
gpio.setmode(gpio.BCM)

gpio.setup(16, OUTPUT)
gpio.setup(18, OUTPUT)
#except:
    #print("GPIO SETUP FAILED!, EXITING TO PREVENT FUTURE PROBLEMS")
    #exit()

print("GPIO SETUP COMPLETE")

print("Setting up HTTP WEB SERVICE")
hName = "localhost"
Port = 8080
class wser (BaseHTTPRequestHandler):
    def do_GET (self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>CS Day Wheeler</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Web server</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
if __name__ == "__main__":
    wser = HTTPServer ((hName, Port), wser)
    print("Web server started http://%s:%s" % (hName, Port))

print("Setting up HTTP SOCKET API")