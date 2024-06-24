import dxcam
import numpy as np
from threading import Thread
from time import perf_counter
import subprocess
import pyfastscreencap_tezzary.settingsfiller as settingsfiller

def _accurate_sleep(seconds):
    start = perf_counter()
    while perf_counter() - start < seconds:
        pass

class Recorder:
    def __init__(self, path="video.mp4", monitor=0, fps=60, bitrate=50, nvenc=False):
        '''
        path: Path to save the video file to
        monitor: Index of the monitor to record from starting at 0
        fps: Frames per second to record at
        bitrate: Bitrate to record at in megabits per second
        nvenc: Whether to use NVENC hardware encoding or not only works with Nvidia GPUs
        '''
        self.path = path
        self.fps = fps
        self.camera = dxcam.create(output_idx=monitor, output_color="BGR")
        test_screenshot = self.camera.grab()
        self.width = test_screenshot.shape[1]
        self.height = test_screenshot.shape[0]
        if nvenc:
            self.encoder = subprocess.Popen(
                settingsfiller.nvenc(self.width, self.height, fps, bitrate, path),
                stdin=subprocess.PIPE
            )
        else:
            self.encoder = subprocess.Popen(
                settingsfiller.x264(self.width, self.height, fps, bitrate, path),
                stdin=subprocess.PIPE
            )
        self.thread = None
        self.recording = False
        self.frame_count = 0

    
    def _start_recording(self):
        start_time = perf_counter()
        self.frame_count = 0
        self.recording = True
        frame = None
        frame_time = perf_counter()
        while self.recording:
            temp_frame = self.camera.grab()
            
            #check for None as will be the case occasionally if fps is set near monitor refresh rate or higher. e.g. 60hz monitor recording with dxcam sometimes can only grab 50-55 frames per second, or 120 hz monitor recording with dxcam sometimes can only grab 100-110 frames per second.
            if(temp_frame is not None):
                frame = temp_frame

            if(frame is not None):
                self.frame_count += 1
                self.encoder.stdin.write(
                    frame
                    .astype(np.uint8)
                    .tobytes()
                )
                _accurate_sleep(start_time + self.frame_count / self.fps - perf_counter())
            print(f"Frame Time: {perf_counter() - frame_time}")
            frame_time = perf_counter()

    def start_recording(self):
        if self.thread:
            print("Attempted to start recording when already recording")
        self.thread = Thread(target=self._start_recording)
        self.thread.start()

    def stop_recording(self):
        if not self.thread:
            print("Attempted to stop recording when not recording")
            return
        self.recording = False
        self.thread.join()
        self.thread = None
        self.camera.stop()
        self.encoder.stdin.close()
        self.encoder.wait()
        return self.frame_count