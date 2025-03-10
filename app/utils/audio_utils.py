import ffmpeg
import tempfile
import io
import soundfile as sf
import torchaudio
import torch
from app.models.model_loader import load_or_save_model

processor, model = load_or_save_model()

SAMPLE_RATE = 16000
VALID_AUDIO_FORMATS = ["wav", "mp3", "flac", "ogg", "m4a"]

def convert_wav(audio_data: bytes):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav.write(audio_data)
        temp_wav_path = temp_wav.name
    
    # Convert to PCM 16-bit WAV
    output_wav_path = temp_wav_path.replace(".wav", "_converted.wav")
    ffmpeg.input(temp_wav_path).output(output_wav_path, format='wav', acodec='pcm_s16le').run(overwrite_output=True)
    
    with open(output_wav_path, 'rb') as converted_file:
        converted_audio_data = converted_file.read()

    return converted_audio_data

def get_file_extension(filename: str):
    return filename.split(".")[-1].lower()



def transcribe_audio(audio_data: bytes, filename: str):
    try:
        file_ext = get_file_extension(filename)
        print(f"Received file: {filename}, Format: {file_ext}")

        if file_ext not in VALID_AUDIO_FORMATS:
            return f"Error: Unsupported file format: {file_ext}"
        
        # Convert to WAV for consistent processing
        audio_data = convert_wav(audio_data)
        audio_stream = io.BytesIO(audio_data)
        
        # Attempt to load using `torch`audio with better error handling
        try:
            waveform, sample_rate = torchaudio.load(audio_stream, format="wav")
            print(f"Initial load - Sample Rate: {sample_rate}, Shape: {waveform.shape}")
            
            # Check if we have a multi-channel audio and convert to mono if needed
            if waveform.dim() > 1 and waveform.shape[0] > 1:
                print(f"Converting {waveform.shape[0]} channels to mono")
                waveform = torch.mean(waveform, dim=0, keepdim=True)
                print(f"After mono conversion - Shape: {waveform.shape}")
                
        except Exception as e:
            print(f"Torchaudio load failed: {e}")
            # Fallback to soundfile
            try:
                audio_stream.seek(0)  # Reset stream position
                waveform, sample_rate = sf.read(audio_stream, dtype="float32")
                print(f"SF load - Sample Rate: {sample_rate}, Shape: {waveform.shape}")
                
                # Handle soundfile's format which might be different
                if len(waveform.shape) > 1 and waveform.shape[1] > 1:
                    print(f"Converting {waveform.shape[1]} channels to mono")
                    waveform = np.mean(waveform, axis=1)
                
                # Convert numpy array to tensor and ensure correct shape (1, n)
                waveform = torch.tensor(waveform)
                if waveform.dim() == 1:
                    waveform = waveform.unsqueeze(0)  # Add channel dimension
                print(f"After tensor conversion - Shape: {waveform.shape}")
                
            except Exception as sf_error:
                print(f"Soundfile load failed: {sf_error}")
                return f"Error: Could not process audio file. {sf_error}"

        # Resample if necessary
        if sample_rate != SAMPLE_RATE:
            print(f"Resampling from {sample_rate} to {SAMPLE_RATE}")
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=SAMPLE_RATE)
            waveform = resampler(waveform)
            print(f"After resampling - Shape: {waveform.shape}")

        # Ensure correct shape for the processor
        print(f"Final waveform shape before processor: {waveform.shape}")
        
        try:
            # Make sure waveform is float32 and in the correct range
            if waveform.dtype != torch.float32:
                waveform = waveform.to(torch.float32)
            
            # Normalize if needed (Whisper expects values roughly in [-1, 1])
            if waveform.abs().max() > 1.0:
                waveform = waveform / waveform.abs().max()
            
            # Try to process with more careful error handling
            try:
                input_features = processor(
                    waveform, 
                    sampling_rate=SAMPLE_RATE, 
                    return_tensors="pt"
                ).input_features
                print(f"Processor output shape: {input_features.shape}")
            except Exception as proc_error:
                print(f"Processor error: {proc_error}")
                # Try an alternative approach - explicitly calling feature extractor
                try:
                    print("Attempting alternative processing approach")
                    # Make a flattened version for the processor
                    flat_waveform = waveform.squeeze().numpy()
                    input_features = processor.feature_extractor(
                        flat_waveform, 
                        sampling_rate=SAMPLE_RATE, 
                        return_tensors="pt"
                    ).input_features
                    print(f"Alternative processor output shape: {input_features.shape}")
                except Exception as alt_error:
                    return f"Error: Feature extraction failed. {alt_error}"
            
            # Generate transcription
            with torch.no_grad():
                predicted_ids = model.generate(input_features)
            
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            return transcription
            
        except Exception as proc_error:
            print(f"Model processing error: {proc_error}")
            import traceback
            traceback.print_exc()
            return f"Error: Failed during model processing. {proc_error}"

    except Exception as e:
        print(f"General transcription error: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"
