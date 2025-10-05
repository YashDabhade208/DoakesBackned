"""
Real-time audio processing for AI Audio Listener.
"""

import asyncio
import logging
import numpy as np
from typing import Optional, Callable, Any
import wave
import io

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handles real-time audio processing and buffering."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_buffer = []
        self.is_recording = False
        self.on_audio_chunk: Optional[Callable] = None

    def start_recording(self):
        """Start audio recording."""
        self.is_recording = True
        self.audio_buffer = []
        logger.info("Audio recording started")

    def stop_recording(self):
        """Stop audio recording."""
        self.is_recording = False
        logger.info("Audio recording stopped")

    def process_audio_chunk(self, audio_data: bytes):
        """Process an audio chunk."""
        if not self.is_recording:
            return

        # Convert bytes to numpy array for processing
        try:
            # Assuming 16-bit PCM audio
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Add to buffer
            self.audio_buffer.append(audio_array)

            # Call the callback function if set
            if self.on_audio_chunk:
                asyncio.create_task(self.on_audio_chunk(audio_array))

        except Exception as e:
            logger.error(f"Error processing audio chunk: {str(e)}")

    def get_audio_data(self) -> Optional[bytes]:
        """Get the current audio buffer as WAV bytes."""
        if not self.audio_buffer:
            return None

        try:
            # Concatenate all audio chunks
            audio_data = np.concatenate(self.audio_buffer)

            # Create WAV file in memory
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())

            return buffer.getvalue()

        except Exception as e:
            logger.error(f"Error creating WAV data: {str(e)}")
            return None

    def clear_buffer(self):
        """Clear the audio buffer."""
        self.audio_buffer = []
        logger.info("Audio buffer cleared")

    def set_audio_chunk_callback(self, callback: Callable[[np.ndarray], Any]):
        """Set callback function for audio chunks."""
        self.on_audio_chunk = callback
