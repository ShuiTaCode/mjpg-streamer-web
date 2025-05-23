import cv2
import threading
import time

class CameraManager:
    _instances = {}
    _locks = {}
    _refcounts = {}

    @classmethod
    def get_camera(cls, device, retries=10, delay=0.2):
        for attempt in range(retries):
            if device not in cls._locks:
                cls._locks[device] = threading.Lock()
            with cls._locks[device]:
                if device not in cls._instances or not cls._instances[device].isOpened():
                    cap = cv2.VideoCapture(device)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cls._instances[device] = cap
                    cls._refcounts[device] = 0
                if cls._instances[device].isOpened():
                    cls._refcounts[device] += 1
                    return cls._instances[device]
            time.sleep(delay)
        # Nach allen Versuchen: None zurückgeben
        return None

    @classmethod
    def release_camera(cls, device):
        if device in cls._locks:
            with cls._locks[device]:
                if device in cls._refcounts:
                    cls._refcounts[device] -= 1
                    if cls._refcounts[device] <= 0:
                        if device in cls._instances:
                            cls._instances[device].release()
                            del cls._instances[device]
                        del cls._refcounts[device] 