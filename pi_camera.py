class PiCamera:
    def __init__(self, device=0):
        try:
            from picamera2 import Picamera2
            from libcamera import controls
        except ImportError as error:
            raise RuntimeError(
                "Pi capture requires Picamera2 and libcamera on Raspberry Pi OS. "
                "See the README setup commands."
            ) from error

        self.camera = Picamera2(camera_num=device)
        try:
            config = self.camera.create_video_configuration(
                main={"size": (1280, 720), "format": "RGB888"}
            )
            self.camera.configure(config)
            if "AfMode" in self.camera.camera_controls:
                self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
            self.camera.start()
        except BaseException:
            self.camera.close()
            raise

    def isOpened(self):
        return self.camera is not None

    def read(self):
        # Picamera2 RGB888 arrays use BGR byte order, matching OpenCV.
        frame = self.camera.capture_array("main")
        return frame is not None and frame.size > 0, frame

    def release(self):
        if self.camera is not None:
            camera, self.camera = self.camera, None
            try:
                camera.stop()
            finally:
                camera.close()
