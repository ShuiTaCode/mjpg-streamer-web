# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from mjpg_streamer_web.camera import mjpeg_generator
import glob
import json
import logging
import os
import socketserver

current_device = None

def set_device(device_name):
    global current_device
    print(f"[LOG] set_device called: {device_name}")
    current_device = device_name

class MJPEGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"[LOG] do_GET called: {self.path}")
        logging.info(f"GET {self.path}")
        if self.path.startswith('/set_camera'):
            import urllib.parse
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            device = params.get('device', [None])[0]
            if device:
                set_device(device)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_error(400, 'Invalid device')
            return
        if self.path == '/cameras':
            cameras = sorted(glob.glob('/dev/video*'))
            logging.info(f"Found cameras: {cameras}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(cameras).encode('utf-8'))
            return
        if self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                logging.error(f"Error loading frontend: {e}")
                self.send_error(500, f'Error loading frontend: {e}')
            return
        if self.path == '/stream' or self.path.startswith('/stream?'):
            logging.info(f"Starting MJPEG stream for device {current_device}")
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            for frame in mjpeg_generator(current_device):
                try:
                    self.wfile.write(b"--frame\r\n")
                    self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
                except BrokenPipeError:
                    logging.warning("BrokenPipeError while streaming")
                    break
            return
        self.send_error(404)

    def do_POST(self):
        if self.path == '/set_camera':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            device = post_data.decode('utf-8')
            if device.isdigit():
                set_device(int(device))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_error(400, 'Invalid device')
            return
        self.send_error(404)

class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True

def start_server(host="0.0.0.0", port=8081):
    print("[LOG] Starting server...")
    # Logging for /dev and devices
    dev_exists = os.path.exists('/dev')
    logging.info(f"/dev exists: {dev_exists}")
    if dev_exists:
        video_devices = sorted(glob.glob('/dev/video*'))
        logging.info(f"Found /dev/video* devices at startup: {video_devices}")
        for dev in video_devices:
            try:
                accessible = os.access(dev, os.R_OK | os.W_OK)
                logging.info(f"{dev}: Read/write access: {accessible}")
            except Exception as e:
                logging.error(f"Error checking {dev}: {e}")
        if video_devices:
            global current_device
            current_device = video_devices[0]
    else:
        logging.error("/dev directory not found!")
    server = ThreadingHTTPServer((host, port), MJPEGHandler)
    print(f"📷 MJPEG Streamer running at http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_server()
