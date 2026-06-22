from flask import Flask, request, render_template
from PIL import Image
import os
from werkzeug.utils import secure_filename
from openai import OpenAI
import base64
from dotenv import load_dotenv
import markdown

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
load_dotenv()


def validate_image(image):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    extension = image.filename.rsplit('.', 1)[-1].lower()
    if extension not in allowed_extensions:
        return False
    try:
        img = Image.open(image)
        img.verify()
        image.seek(0)
        return True
    except Exception:
        return False


def save_image(image):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(image.filename))
    image.save(filepath)
    return filepath


def convert_to_base64(filepath):
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def analyze_acne(filepath):
    client = OpenAI()

    image_data = convert_to_base64(filepath)
    extension = filepath.rsplit('.', 1)[-1].lower()
    if extension == 'jpg':
        extension = 'jpeg'

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/{extension};base64,{image_data}'
                        }
                    },
                    {
                        'type': 'text',
                        'text': '''You are a dermatology assistant. Analyze this facial 
                                    image for acne. Provide: 
                                    
                                    1) Acne types present (blackheads,  whiteheads, cystic, etc.)
                                    2) Severity: mild, moderate, severe
                                    3) Affected areas of the face
                                    4) Skincare recommendations and practices
                                    Note that you are not a licensed dermatologist.'''
                    }
                ]
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content


# @app.route('/')
# def home():
#     return 'Hello, this is the home page!'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        image = request.files['userimage']
        if image.filename == '':
            return 'No file selected', 400
        if (validate_image(image) == False):
            return 'Invalid image file', 400
        filepath = save_image(image)
        diagnosis = analyze_acne(filepath)
        diagnosis = markdown.markdown(diagnosis)
        os.remove(filepath)
        return render_template('index.html', diagnosis=diagnosis)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
