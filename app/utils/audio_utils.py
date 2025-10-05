"""
Audio processing utilities for the AI Audio Listener application.
"""

import wave
import io
import logging
import numpy as np
from typing import Optional, Tuple, Dict, Any
import base64

logger = logging.getLogger(__name__)


class AudioUtils:
    """Utility functions for audio processing."""

    @staticmethod
    def get_audio_info(audio_data: bytes) -> Optional[Dict[str, Any]]:
        """
        Extract information from audio data.

        Args:
            audio_data: WAV audio data as bytes

        Returns:
            Dictionary with audio information or None if invalid
        """
        try:
            with io.BytesIO(audio_data) as buffer:
                with wave.open(buffer, 'rb') as wav_file:
                    return {
                        "channels": wav_file.getnchannels(),
                        "sample_width": wav_file.getsampwidth(),
                        "frame_rate": wav_file.getframerate(),
                        "n_frames": wav_file.getnframes(),
                        "duration": wav_file.getnframes() / wav_file.getframerate(),
                        "format": "WAV"
                    }
        except Exception as e:
            logger.error(f"Error getting audio info: {str(e)}")
            return None

    @staticmethod
    def normalize_audio(audio_data: bytes, target_sample_rate: int = 16000) -> Optional[bytes]:
        """
        Normalize audio data to target sample rate.

        Args:
            audio_data: Input audio data
            target_sample_rate: Target sample rate

        Returns:
            Normalized audio data or None if failed
        """
        try:
            with io.BytesIO(audio_data) as buffer:
                with wave.open(buffer, 'rb') as wav_file:
                    # Read audio data
                    frames = wav_file.readframes(wav_file.getnframes())
                    audio_array = np.frombuffer(frames, dtype=np.int16)

                    # For now, just return original if sample rate matches
                    # In a full implementation, you'd use librosa or similar for resampling
                    if wav_file.getframerate() == target_sample_rate:
                        return audio_data

                    logger.warning(f"Audio sample rate conversion not implemented. Current: {wav_file.getframerate()}, Target: {target_sample_rate}")
                    return audio_data

        except Exception as e:
            logger.error(f"Error normalizing audio: {str(e)}")
            return None

    @staticmethod
    def split_audio_chunks(audio_data: bytes, chunk_duration_ms: int = 1000, sample_rate: int = 16000) -> list:
        """
        Split audio data into chunks.

        Args:
            audio_data: Input audio data
            chunk_duration_ms: Duration of each chunk in milliseconds
            sample_rate: Sample rate of audio

        Returns:
            List of audio chunks
        """
        try:
            with io.BytesIO(audio_data) as buffer:
                with wave.open(buffer, 'rb') as wav_file:
                    frames = wav_file.readframes(wav_file.getnframes())
                    audio_array = np.frombuffer(frames, dtype=np.int16)

                    # Calculate chunk size in samples
                    chunk_samples = int((chunk_duration_ms / 1000) * sample_rate)

                    chunks = []
                    for i in range(0, len(audio_array), chunk_samples):
                        chunk = audio_array[i:i + chunk_samples]
                        if len(chunk) > 0:
                            # Convert back to bytes
                            chunk_bytes = chunk.tobytes()
                            chunks.append(chunk_bytes)

                    return chunks

        except Exception as e:
            logger.error(f"Error splitting audio into chunks: {str(e)}")
            return []

    @staticmethod
    def calculate_audio_level(audio_data: bytes) -> float:
        """
        Calculate the audio level (RMS) of audio data.

        Args:
            audio_data: Audio data as bytes

        Returns:
            Audio level as float
        """
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            if len(audio_array) == 0:
                return 0.0

            # Calculate RMS (Root Mean Square)
            rms = np.sqrt(np.mean(audio_array.astype(float) ** 2))
            return float(rms)

        except Exception as e:
            logger.error(f"Error calculating audio level: {str(e)}")
            return 0.0

    @staticmethod
    def is_silence(audio_data: bytes, threshold: float = 100.0) -> bool:
        """
        Check if audio data represents silence.

        Args:
            audio_data: Audio data as bytes
            threshold: Threshold for silence detection

        Returns:
            True if audio is considered silence
        """
        level = AudioUtils.calculate_audio_level(audio_data)
        return level < threshold

    @staticmethod
    def audio_to_base64(audio_data: bytes) -> str:
        """
        Convert audio data to base64 string.

        Args:
            audio_data: Audio data as bytes

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(audio_data).decode('utf-8')

    @staticmethod
    def base64_to_audio(base64_string: str) -> Optional[bytes]:
        """
        Convert base64 string to audio data.

        Args:
            base64_string: Base64 encoded audio data

        Returns:
            Audio data as bytes or None if invalid
        """
        try:
            return base64.b64decode(base64_string)
        except Exception as e:
            logger.error(f"Error decoding base64 audio: {str(e)}")
            return None

    @staticmethod
    def validate_wav_format(audio_data: bytes) -> bool:
        """
        Validate that audio data is in WAV format.

        Args:
            audio_data: Audio data as bytes

        Returns:
            True if valid WAV format
        """
        try:
            with io.BytesIO(audio_data) as buffer:
                with wave.open(buffer, 'rb') as wav_file:
                    return True
        except Exception:
            return False
