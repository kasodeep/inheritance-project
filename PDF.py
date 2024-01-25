from PIL import Image
from fpdf import FPDF
from moviepy.editor import VideoFileClip
from transformers import ViTFeatureExtractor, ViTForImageClassification
import torch
import torchvision.transforms as transforms
from imagehash import phash
import os
import sys

# Initialize the ViT model for text detection
text_feature_extractor = ViTFeatureExtractor.from_pretrained("JuanMa360/text-in-image-detection")
text_model = ViTForImageClassification.from_pretrained("JuanMa360/text-in-image-detection")

def compute_text_probability(frame):
    inputs_text = text_feature_extractor(images=frame, return_tensors="pt")
    outputs_text = text_model(**inputs_text)
    logits_text = outputs_text.logits
    probability_text = torch.nn.functional.softmax(logits_text, dim=1)[0, 2].item()
    return probability_text

def hash_image(image):
    return phash(image)

def classify_frames(frames, confidence_threshold=0.1, hash_threshold=2):
    processed_frames = set()
    important_frames = []

    for i, frame in enumerate(frames):
        # Check if similar frame has already been processed
        image_hash = hash_image(frame)
        if any(phash(frame) - image_hash < hash_threshold for image_hash in processed_frames):
            continue

        # Compute the probability for text detection without normalization
        probability_text = compute_text_probability(frame)

        # Check if the probability is above the threshold
        if probability_text > confidence_threshold:
            processed_frames.add(image_hash)
            important_frames.append(frame)

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

    for i, frame in enumerate(frames):
        image_filename = f"frame_{i + 1}.png"
        frame.save(image_filename, format='PNG')
        pdf.add_page()
        pdf.image(image_filename, x=15, y=15, w=180)
        os.remove(image_filename)

    pdf.output(output_pdf_path)

if __name__ == "__main__":
    video_path = sys.argv[1]
    output_pdf_path = 'pdf.pdf'

    frames = extract_frames(video_path, num_frames=20)
    important_frames = classify_frames(frames)

    if important_frames:
        generate_pdf(important_frames, output_pdf_path)
        print(f"PDF generated successfully at {output_pdf_path}")
    else:
        print("No important frames found.")