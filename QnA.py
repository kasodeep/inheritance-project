
def extract_text_from_pdf(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text



def ask_question(context, question):
    from transformers import pipeline

    # Load the question-answering pipeline with the deepset/roberta-base-squad2 model
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", tokenizer="deepset/roberta-base-squad2")
    # Use the question-answering model to get an answer
    result = qa_pipeline(context=context, question=question, max_length=512)  # Increase max_length
    answer = result['answer']

    return answer

# Example usage
def run(question):
    text = extract_text_from_pdf(r"transcript_output.pdf")
    answer = ask_question(text, question)
    print("done")
    return answer

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        print('reached flask')
        try:
            data = request.json
            return run(data["question"])
        except Exception as e:
            print(f"Error processing request: {e}")
            
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
   app.run(debug=True,port=4000)