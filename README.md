![PyPI Downloads](https://static.pepy.tech/badge/pyfastscreencap)
# pyfastscreencap

This is a screen recorder in Python that takes advantage of dxcam and ffmpeg to heavily speed up the screen recording process to reach much higher fps counts than you could otherwise reach.

## Install
`
pip install pyfastscreencap
`
## Example

```python
from pyfastscreencap import pyfastscreencap as screencap
from time import sleep

recorder = screencap.Recorder("video.mp4", 0, 120, 50, True)

recorder.start_recording()

sleep(5)

frame_count = recorder.stop_recording()

print(f"Recorded {frame_count} frames")
```

## Limitations

- This screen recorder only works on Windows, this is due to one of its key dependencies [DXCam](https://github.com/ra1nty/DXcam) which only supports Windows due to its low level Windows API usage. This project highly depends on this library due to its blazingly fast screenshot capabilities and any alternatives found currently would seriously degrade performance.

- This screen recorder does not currently record audio but may be used in the future.