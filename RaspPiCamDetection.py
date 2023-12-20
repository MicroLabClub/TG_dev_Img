import time
import http.client
import os
import picamera

DEVICE_ID = 1
host = "172.17.10.22"
port = 5000

image_resolution = (320, 240)

def start_capture(camera, file_name):
    camera.capture(file_name)

def post_image(file_name):
    try:
        conn = http.client.HTTPConnection(host, port)

        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        }

        with open(file_name, 'rb') as file:
            image_data = file.read()

        payload = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
            'Content-Type: image/jpeg\r\n\r\n' +
            image_data.decode('ISO-8859-1') +
            f'\r\n--{boundary}--\r\n'
        )

        conn.request("POST", "/uploads", payload.encode('ISO-8859-1'), headers)
        response = conn.getresponse()

        if response.status == 200:
            print("Image uploaded successfully")
        else:
            print(f"Failed to upload image. Status code: {response.status}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()

def setup():
    print("Setting up...")

def loop():
    print("Capturing and posting image...")
    file_name = time.strftime("%a_%b_%d_%H:%M:%S_%Y", time.localtime()) + ".jpg"

    with picamera.PiCamera() as camera:
        camera.resolution = image_resolution
        time.sleep(2) 
        start_capture(camera, file_name)
        post_image(file_name)

    time.sleep(1800)

if __name__ == "__main__":
    setup()
    while true:
        loop()