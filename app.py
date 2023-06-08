from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from flask import Flask, request, render_template, send_file
import io

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit():
    # Mengambil file gambar dari form
    image_file = request.files['image']
    image = Image.open(image_file)

    # Mendapatkan daftar fitur yang akan digunakan
    features = request.form.getlist('feature')

    # Memeriksa fitur yang dipilih dan menerapkan editing yang sesuai
    if 'crop' in features:
        if 'x1' in request.form and 'y1' in request.form and 'x2' in request.form and 'y2' in request.form:
            box = (int(request.form['x1']), int(request.form['y1']),
                   int(request.form['x2']), int(request.form['y2']))
            image = image.crop(box)

    if 'blur' in features:
        image = image.filter(ImageFilter.BLUR)

    if 'grayscale' in features:
        image = image.convert('L')

    if 'potrait' in features:
        if 'direction' in request.form:
            angle = 0
            if request.form['direction'] == 'clockwise':
                angle = 90
            elif request.form['direction'] == 'counterclockwise':
                angle = -90
            image = image.rotate(angle, expand=True)

    if 'exposure' in features:
        if 'exposure_value' in request.form:
            factor = float(request.form['exposure_value'])
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(factor)

    if 'contrast' in features:
        if 'contrast_value' in request.form:
            factor = float(request.form['contrast_value'])
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(factor)

    # Mengubah gambar yang diedit menjadi byte stream
    image_io = io.BytesIO()
    image.save(image_io, 'JPEG')
    image_io.seek(0)

    return send_file(image_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
  