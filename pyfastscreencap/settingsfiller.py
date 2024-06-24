import os

ffmpeg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'binaries/ffmpeg')

def x264(width, height, fps, bitrate, path):
    return [
            ffmpeg_path,  # Path to ffmpeg executable
            '-f', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', f'{width}x{height}',
            '-r', str(fps),
            '-i', 'pipe:',
            '-pix_fmt', 'yuv420p',
            '-vcodec', 'libx264',
            '-movflags', 'faststart',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-cbr', 'true',
            '-b:v', f'{bitrate}M',
            '-g', str(fps),
            '-y',  # Overwrite output file if it exists
            path
        ]

def nvenc(width, height, fps, bitrate, path):
    return [
            ffmpeg_path,  # Path to ffmpeg executable
            '-f', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', f'{width}x{height}',
            '-r', str(fps),
            '-i', 'pipe:',
            '-pix_fmt', 'yuv420p',
            '-c:v', 'h264_nvenc',
            '-movflags', 'faststart',
            '-preset', '12',  # You can specify preset values here, or use 'fast' as an example
            '-tune', '3',
            '-b:v', f'{bitrate}M',
            '-g', str(fps),
            '-y',  # Overwrite output file if it exists
            path
        ]