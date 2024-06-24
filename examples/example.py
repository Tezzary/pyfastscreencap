import main
from time import sleep
recorder = main.Recorder("video.mp4", 0, 120, 50, True)

recorder.start_recording()

sleep(5)

frame_count = recorder.stop_recording()

print(f"Recorded {frame_count} frames")