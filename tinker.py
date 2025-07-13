import RPi.GPIO as GPIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import time
import os

# GPIO setup
VIBRATION_PIN = 17  # Adjust based on your wiring
GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_PIN, GPIO.IN)

# Email credentials and settings
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "receiver_email@gmail.com"
APP_PASSWORD = "your_app_password"
USB_PATH = "/media/usb"

# Get the most recent video from today's folder
def get_latest_video():
    today_folder = os.path.join(USB_PATH, datetime.now().strftime('%Y-%m-%d'))
    if not os.path.exists(today_folder):
        return None
    videos = sorted([f for f in os.listdir(today_folder) if f.endswith(".h264")], reverse=True)
    if videos:
        return os.path.join(today_folder, videos[0])
    return None

# Send email with video attachment
def send_email(video_path):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "🚨 Crash Detected - RPI Dashcam Alert"

    part = MIMEBase('application', 'octet-stream')
    with open(video_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(video_path)}"')
    msg.attach(part)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

    print(f"✅ Alert sent with video: {video_path}")

# Main crash detection loop
def monitor_crash():
    print("🔍 Crash monitoring started...")
    while True:
        if GPIO.input(VIBRATION_PIN):
            print("Initial vibration detected. Verifying...")

            # Double-check to avoid false triggers
            time.sleep(0.2)
            if GPIO.input(VIBRATION_PIN):
                print("⚠ Strong vibration confirmed! Sending alert...")

                time.sleep(10)  # Debounce period to avoid repeat alerts
                video = get_latest_video()
                if video:
                    send_email(video)
            else:
                print("✖ False alarm ignored.")
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        monitor_crash()
    except KeyboardInterrupt:
        GPIO.cleanup()
