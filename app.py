# -*- coding: utf-8 -*-
"""final_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tZhmyOWDXoaK0loFl56iodNXNFoGdhEh

**Retrieve transcript**
"""

# pip install fpdf
# pip install pytube
# pip install youtube-transcript-api
# pip install fpdf


from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import *

# pip install langdetect
from langdetect import detect

lc=""
def get_transcript(youtube_url, output_pdf_path):
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Try fetching the manual transcript
    try:
        transcript = transcript_list.find_manually_created_transcript()
        language_code = transcript.language_code  # Save the detected language
        lc=language_code
    except:
        # If no manual transcript is found, try fetching an auto-generated transcript in a supported language
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
            language_code = transcript.language_code  # Save the detected language
            lc=language_code
        except:
            # If no auto-generated transcript is found, raise an exception
            raise Exception("No suitable transcript found.")

    full_transcript = " ".join([part['text'] for part in transcript.fetch()])

    # Save the transcript to a PDF file
    save_to_pdf(full_transcript, language_code, output_pdf_path)

    return full_transcript, language_code  # Return both the transcript and detected language

def save_to_pdf(transcript, language_code, output_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Language Code: {language_code}", ln=True, align='C')
    pdf.ln(10)

    pdf.multi_cell(0, 10, txt=transcript)

    pdf.output(output_pdf_path)

"""**Implement Summarizer**"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install PyMuPDF

# Commented out IPython magic to ensure Python compatibility.
# %pip install transformers
# %pip install pytorch

import fitz
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
    return text

from transformers import BartTokenizer, BartForConditionalGeneration

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

#text- text of transcript

def generate_summary_t5(text, tokenizer,model):

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=1000, min_length=600, length_penalty=1.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    output_pdf_path="summary.pdf"

    save_to_pdf(summary, lc, "output_summary.pdf")


    return summary

"""**Download Video**"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install pytube

from pytube import YouTube
import re

def clean_filename(title):
    # Remove special characters and replace spaces with underscores
    cleaned_title = re.sub(r'[^\w\s]', '', title)
    cleaned_title = cleaned_title.replace(' ', '_')
    return cleaned_title

def download_youtube_video(video_url, output_path):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video
        cleaned_title = clean_filename(yt.title)
        print(f"Downloading: {cleaned_title}")
        video_path = video_stream.download(output_path, filename=cleaned_title)
        print("Download complete")

        return video_path

    except Exception as e:
        print(e)
        return None

"""**Images Slides pdf generation**"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install transformers torchvision imagehash

from PIL import Image
from fpdf import FPDF
from moviepy.editor import VideoFileClip
from transformers import ViTFeatureExtractor, ViTForImageClassification
import torch
from imagehash import phash
import os

text_feature_extractor = ViTFeatureExtractor.from_pretrained("JuanMa360/text-in-image-detection")
text_model = ViTForImageClassification.from_pretrained("JuanMa360/text-in-image-detection")
scene_model = None

def compute_text_probability(frame):
    inputs_text = text_feature_extractor(images=frame, return_tensors="pt")
    outputs_text = text_model(**inputs_text)
    logits_text = outputs_text.logits
    probability_text = torch.nn.functional.softmax(logits_text, dim=1)[0, 2].item()
    return probability_text

def hash_image(image):
    return phash(image)

def classify_frames(frames, confidence_threshold_text=0.985, hash_threshold=10, confidence_threshold_scene=0.5, similarity_threshold=0.5):
    processed_frames = set()
    important_frames = []
    for i, frame in enumerate(frames):

        probability_text = compute_text_probability(frame)


        if probability_text > confidence_threshold_text:
            important_frames.append(frame)
            image_hash = hash_image(frame)
            processed_frames.add(image_hash)


    for i in range(1, len(important_frames)):
        current_frame = important_frames[i]
        previous_frame = important_frames[i - 1]

        similarity = 1.0 - (phash(current_frame) - phash(previous_frame)) / 64.0


        if similarity < similarity_threshold:

            important_frames.append(current_frame)


    for frame in important_frames:
        image_hash = hash_image(frame)


        scene_probability = 0.0
        if scene_model is not None:

            scene_probability = 0.0

        if scene_probability > confidence_threshold_scene:
            processed_frames.add(image_hash)

    return important_frames

def extract_frames(video_path, num_frames=5):
    clip = VideoFileClip(video_path)
    frames = []

    frame_interval = max(int(clip.fps * clip.duration) // num_frames, 5)

    for i in range(0, int(clip.fps * clip.duration), frame_interval):
        frame = clip.get_frame(i / clip.fps)
        pil_image = Image.fromarray(frame.astype('uint8'), mode='RGB')
        frames.append(pil_image)

    return frames

def generate_pdf(frames, output_pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for i in range(0, len(frames), 2):

        pdf.add_page()


        image_filename_1 = f"frame_{i + 1}.png"
        frames[i].save(image_filename_1, format='PNG')

        available_width = pdf.w - 30  # 15 units margin on both sides
        available_height = pdf.h - 30  # 15 units margin on both top and bottom

        # Calculate the aspect ratio of the images
        aspect_ratio_1 = frames[i].width / frames[i].height

        # Calculate the width and height of the first image to fit the available space
        width_1 = min(available_width, frames[i].width)
        height_1 = width_1 / aspect_ratio_1

        # Calculate the x and y positions for the first image
        x_1 = 15  # Left margin
        y_1 = 15  # Top margin

        # Add the first image
        pdf.image(image_filename_1, x=x_1, y=y_1, w=width_1, h=height_1)
        os.remove(image_filename_1)

        # Add the second image if available
        if i + 1 < len(frames):
            image_filename_2 = f"frame_{i + 2}.png"
            frames[i + 1].save(image_filename_2, format='PNG')

            # Calculate the width and height of the second image to fit the available space
            width_2 = min(available_width, frames[i + 1].width)
            height_2 = width_2 / aspect_ratio_1  # Use the same aspect ratio as the first image

            # Calculate the x and y positions for the second image
            x_2 = 15  # Left margin
            y_2 = y_1 + height_1  # Place the second image below the first

            # Add the second image
            pdf.image(image_filename_2, x=x_2, y=y_2, w=width_2, h=height_2)
            os.remove(image_filename_2)

    pdf.output(output_pdf_path)

def images(video_path,output_pdf_path):
    frames = extract_frames(video_path, num_frames=20)
    important_frames = classify_frames(frames)
    if important_frames:
        generate_pdf(important_frames, output_pdf_path)
        print(f"PDF generated successfully at {output_pdf_path}")
    else:
        print("No important frames found.")

"""**Running Functions**"""

def run(url):
    print(type(url),url)
    get_transcript(url,"transcript_output.pdf")
    print(1)
    text = extract_text_from_pdf("transcript_output.pdf")
    print(2)
    summary = generate_summary_t5(text,tokenizer,model)
    print(3)
    video_path=download_youtube_video(url,'video.mp4')
    print(4)
    images(video_path,'slides.pdf')
    print(5)

#https://www.youtube.com/watch?v=reUZRyXxUs4

# pip install flask-cors

import numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import traceback
import os
from zipfile import ZipFile
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
            print(data)
            run(data["url"])
            current_directory = os.getcwd()

            pdf_paths = [
        os.path.join(current_directory, 'slides.pdf'),
        os.path.join(current_directory, 'output_summary.pdf')
        ]
            
            zip_filename = 'pdf_files.zip'
            with ZipFile(zip_filename, 'w') as zip:
                for pdf_path in pdf_paths:
                    zip.write(pdf_path, os.path.basename(pdf_path))
            # os.remove('video.mp4')
            # os.remove('slides.pdf')
            # os.remove('output_summary.pdf')
            return send_file(zip_filename, as_attachment=True)
        except Exception as e:
            print(f"Error processing request: {e}")
            
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500


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
def ask(question):
    text = extract_text_from_pdf(r"transcript_output.pdf")
    answer = ask_question(text, question)
    print("done")
    return answer 

@app.route('/qna', methods=['POST'])
def qna():
    if request.method == 'POST':
        print('reached flask')
        try:
            data = request.json
            return ask(data["question"])
        except Exception as e:
            print(f"Error processing request: {e}")
            
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500



if __name__ == '__main__':
   app.run(debug=True,port=3000)