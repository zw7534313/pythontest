from flask import Flask
from flask import request
import google.generativeai as genai
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import base64

from openai import OpenAI

app = Flask(__name__)
CORS(app)
genai.configure(api_key='AIzaSyBW0hnVev4HsQFOFADGYCjGFHYeYCbn3D8')
model = genai.GenerativeModel('gemini-pro')
modelVision = genai.GenerativeModel('gemini-pro-vision')

client = OpenAI(api_key = "sess-ho9TVlTUU4oHF4c3AMdEHhN8Nj9UgECXppcGW8Hx")

@app.route('/')
def home():
    return 'Hello2'

@app.route('/gettext', methods=['POST'])
def getTextFromGemini2():
    json_data = request.json
    image_data = json_data.get('file', '')
    content = request.json.get('text', '')
    if image_data == '' and content != '':
        response = model.generate_content(content)
        return response.text
    elif image_data != '':
        ind = image_data.index(",")
        idata = image_data[ind+1:]
        bin_image_data = base64.b64decode(idata)
        image = Image.open(BytesIO(bin_image_data))
        response = modelVision.generate_content(image)
        return response.text
    return ''

@app.route('/openai')
def openai():
    print('******************')
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Where was it played?"}])
    print(str(response))
    print('----------------------------')
    content = response.choices[0].message.content
    print('*****')
    print(type(content))
    return content

@app.route('/hi')
def hi():
	print('************')
	return 'hi'

@app.route('/hi2')
def hi2():
	print('************')
	return 'hi2'