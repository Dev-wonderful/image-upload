from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
from cloudinary import config, CloudinaryImage
from cloudinary.uploader import upload, upload_image
import cloudinary.api

config(secure=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http:localhost:5500"]}}, supports_credentials=True)
@app.route("/upload", methods = ['POST'])
def uploads():
    """handle image upload"""
    print('here')
    data = request.files
    print(data)
    image = data.get('image')
    print(image.filename)
    print(type(image))
    # response = upload('https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg', public_id="quickstart_butterfly")
    response = upload(image, use_filename=True)
    print(response)
    # image_src = CloudinaryImage(image.filename).build_url()
    print(response.get('url'))
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


if __name__ == "__main__":
    app.run(debug=True)
