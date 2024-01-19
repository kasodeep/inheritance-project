# pip install fpdf
# pip install pytube
# pip install youtube-transcript-api
# pip install fpdf
# pip install youtube_transcript_api

from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import *

def get_transcript(youtube_url, output_pdf_path):
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Try fetching the manual transcript
    try:
        transcript = transcript_list.find_manually_created_transcript()
        language_code = transcript.language_code  # Save the detected language
    except:
        # If no manual transcript is found, try fetching an auto-generated transcript in a supported language
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
            language_code = transcript.language_code  # Save the detected language
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

# Example usage
output_pdf_path = "transcript_output.pdf"
get_transcript("https://www.youtube.com/watch?v=tsJdXpnl48g&list=RDNStsJdXpnl48g&start_radio=1", output_pdf_path)
