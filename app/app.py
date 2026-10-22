from flask import Flask
from modules import ShannonFano
import os


APP_TOKEN = os.environ.get('APP_TOKEN')
APP_MESSAGE = os.environ.get('APP_MESSAGE')
FLASK_HOST = os.environ.get('FLASK_HOST') 
FLASK_PORT =  os.environ.get('FLASK_PORT')

app = Flask(__name__)

@app.get("/")
def hello():
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shannon Fano</title>
</head>
<body>
    <h2>Shannon Fano Decrypter</h2>
    <ul>
        <li><b>Author:</b> Artyom Tsiganov</li>
        <li><b>Project:</b> Shannon Fano decrypter</li>
        <li><b>Token Configured:</b> {len(APP_TOKEN) == 32}</li>
        <li><b>App Message:</b> {APP_MESSAGE}</li>
    </ul>
</body>
</html>"""

@app.post('/encode-data')
def encode_bytes():
    try:
        data = request.get_data()
        result = ShannonFano.encode(data) # encode(string: bytes) -> bytes:
        return result
    except Exception as e:
        abort(400, description=f"Encoding error: {e}")

@app.post('/decode-data')
def decode_bytes():
    try:
        data = request.get_data()
        result = ShannonFano.decode(data) # decode(string: bytes) -> bytes:
        return result
    except Exception as e:
        abort(400, description=f"Encoding error: {e}")


app.run(host=FLASK_HOST, port=FLASK_PORT)
