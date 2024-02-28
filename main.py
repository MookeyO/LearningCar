#!/usr/bin/env python3
#imports
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import subprocess
# HTML code for the web page
PAGE = """
<html>
<head>
<title>RoboCar</title>
<script>
  function moveForward() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/move_forward", true);
    xhr.send();
  }

  function moveBackward() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/move_backward", true);
    xhr.send();
  }

  function turnLeft() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/turn_left", true);
    xhr.send();
  }

  function turnRight() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/turn_right", true);
    xhr.send();
  }

  function stopMovement() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/stop_movement", true);
    xhr.send();
  }

  function startAutonomous() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/start_autonomous", true);
    xhr.send();
  }

  function cancelAutonomous() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/cancel_autonomous", true);
    xhr.send();
  }
</script>
</head>
<body>
<center><h1>RoboCar</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
<center>
  <button onmousedown="moveForward()" onmouseup="stopMovement()">Move Forward</button>
  <button onmousedown="moveBackward()" onmouseup="stopMovement()">Move Backward</button>
  <button onmousedown="turnLeft()" onmouseup="stopMovement()">Turn Left</button>
  <button onmousedown="turnRight()" onmouseup="stopMovement()">Turn Right</button>
  <button onclick="startAutonomous()">Start Autonomous</button>
  <button onclick="cancelAutonomous()">Cancel Autonomous</button>
</center>
</body>
</html>

"""
#streaming output class that manages the stream of the camera
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
#streaming handler class that handles the streaming of the camera feed to the web page
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == '/move_forward':
            subprocess.Popen(["python3", "moveForward.py"])
            self.send_response(200)
            self.end_headers()
        elif self.path == '/move_backward':
            subprocess.Popen(["python3", "moveBackward.py"])
            self.send_response(200)
            self.end_headers()
        elif self.path == '/turn_left':
            subprocess.Popen(["python3", "turnLeft.py"])
            self.send_response(200)
            self.end_headers()
        elif self.path == '/turn_right':
            subprocess.Popen(["python3", "turnRight.py"])
            self.send_response(200)
            self.end_headers()
        elif self.path == '/stop_movement':
            # You may need to implement this based on how your robot stops
            self.send_response(200)
            self.end_headers()
        elif self.path == '/start_autonomous':
            subprocess.Popen(["python3", "autonomous.py"])
            self.send_response(200)
            self.end_headers()

        elif self.path == '/cancel_autonomous':
        # You need to implement a way to cancel the autonomous script
        # For example, you could kill the subprocess running autonomous.py
            subprocess.Popen(["pkill", "-f", "autonomous.py"])  # This command kills the autonomous.py process
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(404)
            self.end_headers()
#streaming server class that manages the server
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
#main function that starts the camera and the server
with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()