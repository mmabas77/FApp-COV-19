import os
import uuid

from flask import Flask, request, json, jsonify

import model

app = Flask(__name__)

app.secret_key = "cov-19"
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():  # put application's code here
    return jsonify(
        info='Upload files to /upload path Using POST Request , File key is (img)',
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['img']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
        file.save(path)
        result = model.runModel(path)
        os.remove(path)
        return jsonify(
            status='success',
            data=result,
            msg='',
            code=200
        )
        # return render_ #str(model.runModel(path))
    else:
        return jsonify(
            status='fail',
            data=None,
            msg='Method Not Allowed',
            code=405
        )


if __name__ == '__main__':
    app.run()
