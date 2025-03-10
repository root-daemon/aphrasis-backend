import os
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

MODEL_NAME = "openai/whisper-small"  
MODEL_PATH = "app/models/whisper_model"

def load_or_save_model():
    """Loads the Whisper model if saved; otherwise, downloads and saves it."""
    if os.path.exists(MODEL_PATH):
        print("🔄 Loading saved model...")
        processor = WhisperProcessor.from_pretrained(MODEL_PATH)
        model = WhisperForConditionalGeneration.from_pretrained(MODEL_PATH)
    else:
        print("⬇️ Downloading and saving model...")
        processor = WhisperProcessor.from_pretrained(MODEL_NAME)
        model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
        processor.save_pretrained(MODEL_PATH)
        model.save_pretrained(MODEL_PATH)
        print("✅ Model saved successfully!")
    
    return processor, model

# Load or save the model
# processor, model = load_or_save_model()
