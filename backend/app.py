from flask import Flask, request, jsonify
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from safetensors.torch import load_file
import re
import pdfplumber
import docx
from flask_cors import CORS
import logging
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths to Model & Tokenizer
MODEL_PATH = "model/model.safetensors"
CONFIG_PATH = "model/config.json"  # Ensure this exists
TOKENIZER_PATH = "tokenizer/"

# Device Configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# Load Tokenizer (from local files)
try:
    tokenizer = BartTokenizer.from_pretrained(TOKENIZER_PATH)
    print("Tokenizer successfully loaded!")
except Exception as e:
    logger.error(f"Tokenizer loading error: {str(e)}")
    raise RuntimeError("Failed to load tokenizer.")

# Load Model (from local files)
try:
    from transformers import AutoConfig
    config = AutoConfig.from_pretrained(CONFIG_PATH)
    model = BartForConditionalGeneration(config)
    state_dict = load_file(MODEL_PATH)
    model.load_state_dict(state_dict, strict=False)
    model.to(device)
    model.eval()

except Exception as e:
    logger.error(f"Model loading error: {str(e)}")
    raise RuntimeError("Failed to load model.")

def preprocess_text(text):
    """Clean and normalize input text"""
    text = text.replace("<n>", " ")  # Remove unwanted newlines
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\[\d+\]', '', text)  # Remove citation numbers
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove links
    return text

def ensure_complete_sentence(summary):
    """Ensure summary ends with proper punctuation"""
    summary = summary.strip()
    if not summary:
        return summary

    last_punct = max(summary.rfind('.'), summary.rfind('!'), summary.rfind('?'))
    if last_punct != -1:
        return summary[:last_punct + 1]
    return summary

def remove_redundancy(summary):
    summary = re.sub(r'(\b\w+\b(?: \b\w+\b){1,5})( \1)+', r'\1', summary)
    return summary

def calculate_max_length(text, compression_ratio):
    """Dynamically calculate max summary length"""
    words = len(text.split())
    sentences = len(re.split(r'[.!?]', text))

    dynamic_min_length = min(max(words // 10, 50), 512)

    max_length = min(
        int(words * compression_ratio),
        512,
        sentences * 20
    )

    return max(dynamic_min_length, max_length)

def generate_summary(text, compression_ratio):
    """Generate summary with local model"""
    try:
        text = preprocess_text(text)
        if not text:
            return ""

        inputs = tokenizer(
            text,
            max_length=1024,
            truncation=True,
            return_tensors="pt"
        ).to(device)

        max_length = calculate_max_length(text, compression_ratio)
        min_length = max(50, max_length // 2)

        summary_ids = model.generate(
            inputs.input_ids,
            max_length=max_length,
            min_length=min_length,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=3
        )

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary = ensure_complete_sentence(summary)
        summary = remove_redundancy(summary)
        summary = summary.replace("<n>", " ")
        return summary

    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return ""

def extract_text_from_pdf(file):
    """Extract text from PDF"""
    try:
        text = ""
        with pdfplumber.open(BytesIO(file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return preprocess_text(text)
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX"""
    try:
        doc = docx.Document(BytesIO(file.read()))
        return preprocess_text("\n".join(p.text for p in doc.paragraphs if p.text))
    except Exception as e:
        logger.error(f"DOCX processing error: {str(e)}")
        return ""

def extract_text_from_txt(file):
    """Extract text from TXT"""
    try:
        return preprocess_text(file.read().decode('utf-8'))
    except Exception as e:
        logger.error(f"TXT processing error: {str(e)}")
        return ""

@app.route('/')
def index():
    return "<h1>Hello, this is the backend.</h1>"

@app.route('/summarize', methods=['POST'])
def summarize_text():
    """Summarization endpoint"""
    try:
        compression = float(request.form.get('compression_ratio', 0.3))
        compression = max(0.1, min(0.8, compression))

        text = ""

        if 'file' in request.files:
            file = request.files['file']
            ext = file.filename.split('.')[-1].lower()

            processors = {
                'pdf': extract_text_from_pdf,
                'docx': extract_text_from_docx,
                'txt': extract_text_from_txt
            }

            if ext not in processors:
                return jsonify({"error": "Unsupported file type"}), 400

            text = processors[ext](file)

        elif 'text' in request.form:
            text = preprocess_text(request.form['text'])

        if not text or len(text.split()) < 10:
            return jsonify({"error": "Insufficient text for summarization"}), 400

        summary = generate_summary(text, compression)
        if not summary:
            return jsonify({"error": "Summarization failed"}), 500

        return jsonify({"summary": summary})

    except Exception as e:
        logger.error(f"Endpoint error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)