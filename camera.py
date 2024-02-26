import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import subprocess

PAGE = """\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
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

  function stopMovement() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/stop_movement", true);
    xhr.send();
  }
</script>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
<center>
  <button onmousedown="moveForward()" onmouseup="stopMovement()">Move Forward</button>
  <button onmousedown="moveBackward()" onmouseup="stopMovement()">Move Backward</button>
</center>
</body>
</html>
"""

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
            # Call the moveForward.py script
            subprocess.Popen(["python3", "moveForward.py"])
            self.send_response(200)
            self.end_headers()
        elif self.path == '/move_backward':
            # Call the moveBackward.py script
            subprocess.Popen(["python3", "moveBackward.py"])
            self.send_response(200)
            self.end_headers()
        elif self.path == '/stop_movement':
            # You may need to implement this based on how your robot stops
            # For example, you might need to call another script to stop the movement
            # subprocess.Popen(["python3", "stopMovement.py"])
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

