"""
AI analysis service for processing transcribed text.
"""

import asyncio
import logging
import openai
from typing import Dict, Any, List, Optional
import os

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for AI-powered text analysis and insights."""

    def __init__(self):
        self.client = None
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            logger.warning("OpenAI API key not provided. Analysis functionality will be disabled.")

    async def analyze_text(self, text: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze text using AI.

        Args:
            text: Text to analyze
            analysis_type: Type of analysis to perform

        Returns:
            Analysis results
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not initialized",
                "analysis": None
            }

        try:
            if analysis_type == "sentiment":
                prompt = self._build_sentiment_prompt(text)
            elif analysis_type == "summarization":
                prompt = self._build_summarization_prompt(text)
            elif analysis_type == "key_points":
                prompt = self._build_key_points_prompt(text)
            else:
                prompt = self._build_general_prompt(text)

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant for analyzing text."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
            )

            analysis_result = response.choices[0].message.content.strip()

            return {
                "success": True,
                "analysis_type": analysis_type,
                "result": analysis_result,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "analysis": None
            }

    def _build_sentiment_prompt(self, text: str) -> str:
        """Build prompt for sentiment analysis."""
        return f"""
        Analyze the sentiment of the following text and provide a response in JSON format:
        Text: "{text}"

        Please return a JSON object with:
        - sentiment: (positive, negative, neutral, or mixed)
        - confidence: (a score between 0 and 1)
        - emotions: (array of detected emotions like happy, sad, angry, etc.)
        - summary: (brief explanation of the sentiment)
        """

    def _build_summarization_prompt(self, text: str) -> str:
        """Build prompt for text summarization."""
        return f"""
        Please summarize the following text in a concise manner:
        Text: "{text}"

        Provide a summary that captures the main points and key information.
        Keep it under 100 words if possible.
        """

    def _build_key_points_prompt(self, text: str) -> str:
        """Build prompt for extracting key points."""
        return f"""
        Extract the key points and important information from the following text:
        Text: "{text}"

        Return a bullet-point list of the most important points.
        """

    def _build_general_prompt(self, text: str) -> str:
        """Build general analysis prompt."""
        return f"""
        Please analyze the following text and provide insights:
        Text: "{text}"

        Consider aspects like:
        - Main topics discussed
        - Key information
        - Potential implications
        - Overall context

        Provide a comprehensive but concise analysis.
        """

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response using AI.

        Args:
            prompt: User prompt
            context: Optional context for the conversation

        Returns:
            Generated response
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not initialized",
                "response": None
            }

        try:
            messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

            if context:
                messages.append({"role": "assistant", "content": context})

            messages.append({"role": "user", "content": prompt})

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7
                )
            )

            generated_text = response.choices[0].message.content.strip()

            return {
                "success": True,
                "response": generated_text,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

    def is_available(self) -> bool:
        """Check if the analysis service is available."""
        return self.client is not None
