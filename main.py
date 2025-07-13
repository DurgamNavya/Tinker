from picamera2 import Picamera2
from datetime import datetime
import time
import os

# Set your USB mount path
USB_PATH = "/media/usb"

# Create a new folder for today's date if it doesn't exist
def get_today_folder():
    date_folder = os.path.join(USB_PATH, datetime.now().strftime('%Y-%m-%d'))
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)
    return date_folder

# Start continuous video recording
def start_recording():
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}))
    picam2.start()

    while True:
        filename = datetime.now().strftime('%H-%M-%S.h264')
        filepath = os.path.join(get_today_folder(), filename)
        picam2.start_recording(filepath)
        time.sleep(60)  # Record 1-minute clips
        picam2.stop_recording()

if __name__ == "__main__":
    try:
        start_recording()
    except KeyboardInterrupt:
        print("Recording stopped by user.")
