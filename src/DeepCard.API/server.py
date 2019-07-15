from wsgiref.simple_server import make_server
import traceback
import base64
from io import BytesIO
from PIL import Image
from api import get_result
import json
import os

def base64_to_image(base64_str):
    byte_data = base64.b64decode(base64_str)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def application(environ, start_response):
    print("Recieved")

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    try:
        request_body = environ['wsgi.input'].read(request_body_size)
        # print(request_body)
        img = base64_to_image(request_body)
        res = get_result(img)
    except Exception as e:
        res = "Error"
        print(e)
        traceback.print_exc()

    print("Result:", res)

    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps(res).encode("utf-8")]

if __name__ == '__main__':
    print('Server starting...')
    httpd = make_server('', 80, application)
    print('Server running...')
    httpd.serve_forever()