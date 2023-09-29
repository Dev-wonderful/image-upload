from flask import Flask, request, redirect, current_app, send_file
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
from cloudinary import config, CloudinaryImage
from cloudinary.uploader import upload, upload_image
import cloudinary.api
import base64
import os
import re
from io import BytesIO

config(secure=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http:localhost:5500"]}}, supports_credentials=True)
@app.route("/upload", methods = ['POST'])
def uploads():
    """handle image upload"""
    data = request.files
    image = data.get('image')
    # response = upload('https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg', public_id="quickstart_butterfly")
    response = upload(image, use_filename=True)
    # image_src = CloudinaryImage(image.filename).build_url()
    return {'data': response.get('url')}


# @app.route("/uploadfile", methods = ['POST'])
# def uploadfile():
#     """handle image upload"""
#     print('here')
#     data = request.form.get('file')
#     file = request.files
#     print(f'file: {file}')
#     print(f'data: {data}')
#     # image = data.get('image')
#     # print(image.filename)
#     # print(type(image))
#     # # response = upload('https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg', public_id="quickstart_butterfly")
#     # response = upload(image, use_filename=True)
#     # print(response)
#     # # image_src = CloudinaryImage(image.filename).build_url()
#     # print(response.get('url'))
#     # return {'data': response.get('url')}
#     return "success"


@app.route('/video-upload', methods=['POST'])
def upload_video():
    """uplaod video test"""
    file = request.files.get('video')
    print(file.__dict__)
    text = base64.b64encode(file.read())
    # print(text)
    name = file.filename.split(".")
    with open(f"{name[0]}.txt", "wb") as video_base:
        video_base.write(text)
        video_base.close()

        fh = open("video.mp4", "wb")
        # fh = open(f"{file.filename}", "wb")
        fh.write(base64.b64decode(text))
        fh.close()
    return redirect("http://127.0.0.1:5500/app.html")


@app.route('/video', methods=['GET'])
def get_video():
    """get a video"""
    headers = request.headers
    print(f"headers: {headers}")

    video_path = os.path.abspath("video.mp4")
    size = os.stat(video_path)
    size = size.st_size

    chunk_size = (1024) * 3 #1000kb makes 1mb * 3 = 3mb (this is based on your choice)
    if not "Range" in headers:
        start = 0
    else:
        start = int(re.sub("\D", "", headers["Range"]))
    end = min(start + chunk_size, size - 1)

    content_length = end - start + 1

    def get_chunk(video_path, start, chunk_size):
        with open(video_path, "rb") as f:
            f.seek(start)
            chunk = f.read(chunk_size)
        return chunk

    headers = {
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": content_length,
        "Content-Type": "video/mp4",
    }

    return current_app.response_class(get_chunk(video_path, start,chunk_size), 206, headers)


@app.route("/video/download", methods=["GET"])
def download():
    """check if download is possible"""
    video_path = os.path.abspath("video_base.txt")
    with open(video_path, "rb") as file:
        binary_data = file.read()
    
    return send_file(BytesIO(base64.b64decode(binary_data)), download_name="video.mp4")


if __name__ == "__main__":
    app.run(debug=True)
