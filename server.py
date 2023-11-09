from flask import Flask, render_template, request
from functions import get_check_image_url, image_to_ascii
from waitress import serve


app = Flask(__name__, static_url_path='/static')


@app.route('/')
@app.route('/index')
@app.route('/My_Art')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_art')
def get_art():
    image_url = get_check_image_url()
    new_img_data, file_Name = image_to_ascii(image_url, save_image=False)
    file_Name = file_Name.replace("_", " ").title()


    return render_template(
        "new_art.html",
        img_data = new_img_data.decode('utf-8'),
        file_name = file_Name
        )


if __name__ == "__main__":
    #  This is a development server. Do not use it in a production deployment.
    app.run( host="0.0.0.0", port=8000)
    # serve(app, host="0.0.0.0", port=8000)
