
import os

from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url

import requests
import json5

API_URL = "https://api-inference.huggingface.co/models/PriyamSheta/Shakespeare"
headers = {"Authorization": "Bearer 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"}

port = 12345
base_url = get_base_url(port)

if base_url == '/':
  app = Flask(__name__)
else:
  app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()


@app.route(f'{base_url}')
def home():
  return render_template('writer_home.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
  return redirect(url_for('results'))



@app.route(f'{base_url}/results/')
def results():
  if 'data' in session:
    data = session['data']
    return render_template('Write-your-story-with-AI.html', generated=data)
  else:
    return render_template('Write-your-story-with-AI.html', generated=None)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
  """
    view function that will return json response for generated text. 
    """
  prompt = request.form['prompt']
  if prompt is not None:

    payload = {
      "inputs": prompt,
      "parameters": {
        "max_length": 200,
        "top_p": 0.95,
        "temperature": 1.9,
        "repetition_penalty": 1.5
      }
    }

  data = query(payload)
  print(data)
  if data:
    return render_template('Write-your-story-with-AI.html', generated=data)
  else:
    return render_template('Write-your-story-with-AI.html', generated=None)


if __name__ == '__main__':
  website_url = 'coding.ai-camp.dev'

  print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
  app.run(host='0.0.0.0', port=port, debug=True)
