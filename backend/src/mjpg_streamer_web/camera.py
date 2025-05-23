# camera.py
import cv2
import numpy as np
from .camera_manager import CameraManager

def mjpeg_generator(device_index=0):
    print(f"[LOG] mjpeg_generator: Versuche Kamera zu öffnen: {device_index}")
    cap = CameraManager.get_camera(device_index)
    if cap is None or not cap.isOpened():
        print(f"[LOG] Konnte Kamera NICHT öffnen: {device_index}")
        # Platzhalterbild erzeugen
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(img, 'Keine Kamera verfugbar', (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', img)
        yield jpeg.tobytes()
        return
    else:
        print(f"[LOG] Kamera geöffnet: {device_index}")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield jpeg.tobytes()
    finally:
        CameraManager.release_camera(device_index)
        print(f"[LOG] Kamera freigegeben: {device_index}")
