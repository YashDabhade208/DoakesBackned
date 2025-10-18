import os
import time
import logging
import whisper
from pathlib import Path
from datetime import datetime

class WhisperTranscriber:
    def __init__(self, model_size="base"):
        """
        Initialize the Whisper model
        Available models: tiny, base, small, medium, large
        """
        self.model_size = model_size
        self.model = None
        self.load_model()
        
        # Directory setup
        self.base_dir = Path(__file__).parent
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        self.processed_dir = self.base_dir / "processed"
        self.logs_dir = self.base_dir / "logs"
        
        # Ensure directories exist
        for directory in [self.input_dir, self.output_dir, self.processed_dir, self.logs_dir]:
            directory.mkdir(exist_ok=True)
        
        self.setup_logging()
    
    def load_model(self):
        """Load the Whisper model"""
        try:
            print(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.logs_dir / f"transcription_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_supported_formats(self):
        """Return supported audio formats"""
        return ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.mp4', '.avi', '.mov', '.mpeg', '.mpg']
    
    def detect_language(self, audio_path):
        """Detect the language of the audio file"""
        try:
            # Load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(str(audio_path))
            audio = whisper.pad_or_trim(audio)
            
            # Make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
            
            # Detect the spoken language
            _, probs = self.model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            confidence = probs[detected_language]
            
            # Language code to name mapping
            language_names = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
                'zh': 'Chinese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi',
                'tr': 'Turkish', 'nl': 'Dutch', 'pl': 'Polish', 'sv': 'Swedish',
                'fi': 'Finnish', 'no': 'Norwegian', 'da': 'Danish', 'el': 'Greek',
                'he': 'Hebrew', 'th': 'Thai', 'vi': 'Vietnamese', 'id': 'Indonesian',
                'ms': 'Malay', 'fil': 'Filipino', 'uk': 'Ukrainian', 'cs': 'Czech',
                'ro': 'Romanian', 'hu': 'Hungarian', 'bg': 'Bulgarian', 'ca': 'Catalan'
            }
            
            language_name = language_names.get(detected_language, detected_language)
            
            self.logger.info(f"Detected language: {language_name} ({detected_language}) with {confidence:.2%} confidence")
            return detected_language, language_name, confidence
            
        except Exception as e:
            self.logger.error(f"Error detecting language for {audio_path}: {e}")
            return None, "Unknown", 0.0
    
    def transcribe_audio(self, audio_path, language=None, task="transcribe"):
        """
        Transcribe a single audio file with language auto-detection
        
        Args:
            audio_path: Path to audio file
            language: Force specific language (None for auto-detection)
            task: "transcribe" or "translate" (translate to English)
        """
        try:
            self.logger.info(f"Transcribing: {audio_path}")
            
            # Auto-detect language if not specified
            if language is None:
                detected_language, language_name, confidence = self.detect_language(audio_path)
                self.logger.info(f"Auto-detected language: {language_name} (confidence: {confidence:.2%})")
            else:
                detected_language = language
                self.logger.info(f"Using specified language: {language}")
            
            # Transcribe using Whisper
            result = self.model.transcribe(
                str(audio_path),
                language=detected_language if language is None else language,
                task=task,
                fp16=False,  # Set to True if you have CUDA
                verbose=False  # Set to True to see progress
            )
            
            # Extract text and additional information
            transcript = result["text"]
            language_used = result.get("language", detected_language)
            
            self.logger.info(f"Successfully transcribed: {audio_path} (Language: {language_used})")
            
            return {
                "text": transcript,
                "language": language_used,
                "task": task,
                "segments": result.get("segments", [])
            }
            
        except Exception as e:
            self.logger.error(f"Error transcribing {audio_path}: {e}")
            return None
    
    def save_transcript(self, audio_file, transcript_data):
        """Save transcript to output directory with language information"""
        try:
            # Create output filename (same name with .txt extension)
            output_filename = audio_file.stem + ".txt"
            output_path = self.output_dir / output_filename
            
            # Create JSON output for detailed information
            json_filename = audio_file.stem + ".json"
            json_path = self.output_dir / json_filename
            
            # Save detailed transcript with metadata
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"File: {audio_file.name}\n")
                f.write(f"Language: {transcript_data['language']}\n")
                f.write(f"Task: {transcript_data['task']}\n")
                f.write(f"Transcript:\n")
                f.write("=" * 50 + "\n")
                f.write(transcript_data['text'])
                f.write("\n" + "=" * 50 + "\n")
            
            # Save JSON with segments and timing information
            import json
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'file': audio_file.name,
                    'language': transcript_data['language'],
                    'task': transcript_data['task'],
                    'text': transcript_data['text'],
                    'segments': transcript_data['segments']
                }, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Transcript saved: {output_path}")
            self.logger.info(f"Detailed JSON saved: {json_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error saving transcript: {e}")
            return None
    
    def move_processed_file(self, audio_path):
        """Move processed file to processed directory"""
        try:
            processed_path = self.processed_dir / audio_path.name
            audio_path.rename(processed_path)
            self.logger.info(f"Moved to processed: {processed_path}")
        except Exception as e:
            self.logger.error(f"Error moving file: {e}")
    
    def process_single_file(self, audio_path, language=None, task="transcribe"):
        """Process a single audio file with language options"""
        # Check if already processed
        output_file = self.output_dir / (audio_path.stem + ".txt")
        if output_file.exists():
            self.logger.info(f"Already processed: {audio_path}")
            self.move_processed_file(audio_path)
            return True
        
        # Transcribe
        transcript_data = self.transcribe_audio(audio_path, language, task)
        
        if transcript_data:
            # Save transcript
            self.save_transcript(audio_path, transcript_data)
            
            # Move to processed
            self.move_processed_file(audio_path)
            return True
        else:
            return False
    
    def get_available_languages(self):
        """Return list of available languages supported by Whisper"""
        return {
            'en': 'English', 'zh': 'Chinese', 'de': 'German', 'es': 'Spanish', 
            'ru': 'Russian', 'ko': 'Korean', 'fr': 'French', 'ja': 'Japanese',
            'pt': 'Portuguese', 'tr': 'Turkish', 'pl': 'Polish', 'ca': 'Catalan',
            'nl': 'Dutch', 'ar': 'Arabic', 'sv': 'Swedish', 'it': 'Italian',
            'id': 'Indonesian', 'hi': 'Hindi', 'fi': 'Finnish', 'vi': 'Vietnamese',
            'he': 'Hebrew', 'uk': 'Ukrainian', 'el': 'Greek', 'ms': 'Malay',
            'cs': 'Czech', 'ro': 'Romanian', 'da': 'Danish', 'hu': 'Hungarian',
            'ta': 'Tamil', 'no': 'Norwegian', 'th': 'Thai', 'ur': 'Urdu',
            'hr': 'Croatian', 'bg': 'Bulgarian', 'lt': 'Lithuanian', 'la': 'Latin',
            'mi': 'Maori', 'ml': 'Malayalam', 'cy': 'Welsh', 'sk': 'Slovak',
            'te': 'Telugu', 'fa': 'Persian', 'lv': 'Latvian', 'bn': 'Bengali',
            'sr': 'Serbian', 'az': 'Azerbaijani', 'sl': 'Slovenian', 'kn': 'Kannada',
            'et': 'Estonian', 'mk': 'Macedonian', 'br': 'Breton', 'eu': 'Basque',
            'is': 'Icelandic', 'hy': 'Armenian', 'ne': 'Nepali', 'mn': 'Mongolian',
            'bs': 'Bosnian', 'kk': 'Kazakh', 'sq': 'Albanian', 'sw': 'Swahili',
            'gl': 'Galician', 'mr': 'Marathi', 'pa': 'Punjabi', 'si': 'Sinhala',
            'km': 'Khmer', 'sn': 'Shona', 'yo': 'Yoruba', 'so': 'Somali',
            'af': 'Afrikaans', 'oc': 'Occitan', 'ka': 'Georgian', 'be': 'Belarusian',
            'tg': 'Tajik', 'sd': 'Sindhi', 'gu': 'Gujarati', 'am': 'Amharic',
            'yi': 'Yiddish', 'lo': 'Lao', 'uz': 'Uzbek', 'fo': 'Faroese',
            'ht': 'Haitian Creole', 'ps': 'Pashto', 'tk': 'Turkmen', 'nn': 'Nynorsk',
            'mt': 'Maltese', 'sa': 'Sanskrit', 'lb': 'Luxembourgish', 'my': 'Myanmar',
            'bo': 'Tibetan', 'tl': 'Tagalog', 'mg': 'Malagasy', 'as': 'Assamese',
            'tt': 'Tatar', 'haw': 'Hawaiian', 'ln': 'Lingala', 'ha': 'Hausa',
            'ba': 'Bashkir', 'jw': 'Javanese', 'su': 'Sundanese'
        }
    
    def monitor_and_process(self, interval=10, language=None, task="transcribe"):
        """Monitor input directory for new files with language options"""
        self.logger.info(f"Starting directory monitoring... (Language: {language or 'Auto-detect'}, Task: {task})")
        
        while True:
            try:
                # Get all supported audio files
                supported_formats = self.get_supported_formats()
                audio_files = []
                
                for format in supported_formats:
                    audio_files.extend(self.input_dir.glob(f"*{format}"))
                
                if audio_files:
                    self.logger.info(f"Found {len(audio_files)} files to process")
                
                # Process each file
                for audio_file in audio_files:
                    self.process_single_file(audio_file, language, task)
                
                # Wait before next check
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Whisper Multi-language Transcription')
    parser.add_argument('--model', default='base', help='Whisper model size (tiny, base, small, medium, large)')
    parser.add_argument('--language', help='Force specific language (e.g., "en", "es", "fr"). Leave empty for auto-detection')
    parser.add_argument('--task', default='transcribe', choices=['transcribe', 'translate'], 
                       help='Transcribe or translate to English')
    parser.add_argument('--file', help='Specific file to process (optional)')
    
    args = parser.parse_args()
    
    # Initialize transcriber
    transcriber = WhisperTranscriber(model_size=args.model)
    
    # List available languages if requested
    if args.language == 'list':
        languages = transcriber.get_available_languages()
        print("Available languages:")
        for code, name in sorted(languages.items()):
            print(f"  {code}: {name}")
        return
    
    # Process specific file or all files
    if args.file:
        audio_file = transcriber.input_dir / args.file
        if audio_file.exists():
            transcriber.logger.info(f"Processing file: {audio_file}")
            transcriber.process_single_file(audio_file, args.language, args.task)
        else:
            transcriber.logger.error(f"File not found: {audio_file}")
    else:
        # Process all files in input directory
        supported_formats = transcriber.get_supported_formats()
        processed_count = 0
        
        for format in supported_formats:
            for audio_file in transcriber.input_dir.glob(f"*{format}"):
                if transcriber.process_single_file(audio_file, args.language, args.task):
                    processed_count += 1
        
        transcriber.logger.info(f"Processing completed. Processed {processed_count} files.")
    
    transcriber.logger.info("Transcription completed.")

if __name__ == "__main__":
    main()