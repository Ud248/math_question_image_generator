import asyncio
import time
import os
import json
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from fastapi import HTTPException
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class DeepSeekService:
    def __init__(self):
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://ark.ap-southeast.bytepluses.com/api/v3")
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "tuyen_edulive")
        self.model = os.getenv("DEEPSEEK_MODEL", "ep-20250429194234-4m2tz")
        self.client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key)
        # Connection pool for better concurrent performance
        self.session = None
        
        self.timeout = 100.0
        self.max_retries = 3
        self.retry_delay = 1.0
        self.last_call_duration = 0.0
        self.total_calls = 0
        self.total_time = 0.0
        
        # Updated System Prompt for a reliable AI Agent
        self.system_prompt = (
            "You are a highly intelligent AI agent. Your primary function is to follow instructions precisely. "
            "When asked to produce a JSON object, you must output ONLY the JSON object and nothing else. "
            "Do not include any explanatory text, markdown formatting, or any characters outside of the JSON structure."
        )
        
        self.stop_sequences = ["\nUser:", "\nAssistant:", "</s>"]
    
    async def _ensure_session(self):
        """Ensure aiohttp session is available for concurrent requests"""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,  # Total connection pool size
                limit_per_host=20,  # Max connections per host
                ttl_dns_cache=300,  # DNS cache TTL
                use_dns_cache=True,
            )
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
    
    async def close_session(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    def _extract_json_from_response(self, text: str) -> Optional[str]:
        """Extracts a JSON block from a string, even if it's embedded in markdown."""
        if not text:
            return None
        # Find the start of the JSON block
        json_start = text.find('{')
        if json_start == -1:
            return None
        # Find the end of the JSON block
        json_end = text.rfind('}')
        if json_end == -1 or json_end < json_start:
            return None
        # Extract and return the JSON string
        return text[json_start:json_end + 1]

    async def _make_request_with_retry(self, messages: list, is_json_mode: bool) -> Optional[str]:
        """Make request with retry mechanism, now with JSON mode support."""
        start_time = time.perf_counter()
        
        request_params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4096, # Increased for complex JSON
            "temperature": 0.0,
            "top_p": 1.0,
            "n": 1,
            "stop": self.stop_sequences
        }
        
        if is_json_mode:
            request_params["response_format"] = {"type": "json_object"}

        for attempt in range(self.max_retries):
            try:
                attempt_start_time = time.perf_counter()
                print(f"🚀 Local Model API call attempt {attempt + 1}/{self.max_retries} started (JSON Mode: {is_json_mode})")
                
                response = await self.client.chat.completions.create(**request_params)
                content = response.choices[0].message.content if response.choices and response.choices[0].message else ""
                content = (content or "").strip()
                
                attempt_duration = time.perf_counter() - attempt_start_time
                total_duration = time.perf_counter() - start_time
                
                if content:
                    print(f"✅ Local Model API call successful - Attempt {attempt + 1} duration: {attempt_duration:.2f}s, Total duration: {total_duration:.2f}s")
                    return content
                
                print(f"⚠️ Local Model API call failed (empty response) - Attempt {attempt + 1} duration: {attempt_duration:.2f}s")
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"⏳ Retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                attempt_duration = time.perf_counter() - attempt_start_time
                print(f"💥 Local Model API error: {str(e)} - Attempt {attempt + 1} duration: {attempt_duration:.2f}s")
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"⏳ Retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)
                
        total_duration = time.perf_counter() - start_time
        print(f"❌ Local Model API call failed after all retries - Total duration: {total_duration:.2f}s")
        return None

    async def generate_message(self, prompt: str, is_json_mode: bool = True) -> str:
        """
        Generate a message using local model, with an option for JSON mode.
        Now supports true concurrent requests with connection pooling.
        """
        start_time = time.perf_counter()
        print(f"📝 Starting Local Model message generation (JSON Mode: {is_json_mode})...")
        
        if not prompt or not prompt.strip():
            print("⚠️ Empty prompt provided")
            return json.dumps({"error": "Empty prompt provided"}) if is_json_mode else "Error: Empty prompt provided"

        try:
            # Ensure session is available for concurrent requests
            await self._ensure_session()
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt.strip()}
            ]
            
            result = await self._make_request_with_retry(messages, is_json_mode)
            
            total_duration = time.perf_counter() - start_time
            
            if result is None:
                print(f"❌ Failed to get response from Local Model API - Total duration: {total_duration:.2f}s")
                self._update_stats(total_duration, False)
                return json.dumps({"error": "Failed to get response from Local Model API"}) if is_json_mode else "Error: Failed to get response from Local Model API"
            
            # If in JSON mode, try to extract the JSON part to be safe
            if is_json_mode:
                extracted_json = self._extract_json_from_response(result)
                if not extracted_json:
                    print(f"⚠️ Could not extract valid JSON from response: {result}")
                    self._update_stats(total_duration, False)
                    return json.dumps({"error": "Invalid JSON in response", "response": result})
                result = extracted_json

            self._update_stats(total_duration, True)
            print(f"✅ Local Model message generation completed successfully!")
            return result
            
        except Exception as e:
            total_duration = time.perf_counter() - start_time
            print(f"💥 Error occurred while generating message: {str(e)} - Duration: {total_duration:.2f}s")
            self._update_stats(total_duration, False)
            # Return a JSON error object if in JSON mode
            if is_json_mode:
                return json.dumps({"error": f"An unexpected error occurred: {e}"})
            raise HTTPException(status_code=500, detail=f"Máy chủ đang bận, vui lòng thử lại sau")

    # ... (rest of the helper methods like _update_stats, get_call_stats, etc. remain the same) ...
    def _update_stats(self, duration: float, success: bool) -> None:
        """Update call statistics."""
        self.last_call_duration = duration
        self.total_calls += 1
        self.total_time += duration
        
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"📈 Call stats updated - {status} | Duration: {duration:.2f}s | Total calls: {self.total_calls}")

    def get_call_stats(self) -> Dict[str, Any]:
        """Get comprehensive call statistics."""
        return {
            "last_call_duration": self.last_call_duration,
            "total_calls": self.total_calls,
            "total_time": self.total_time,
            "average_duration": self.get_average_call_duration(),
            "model": self.model
        }

    def get_average_call_duration(self) -> float:
        """Get average call duration."""
        if self.total_calls == 0:
            return 0.0
        return self.total_time / self.total_calls

    def reset_stats(self) -> None:
        """Reset all call statistics."""
        self.last_call_duration = 0.0
        self.total_calls = 0
        self.total_time = 0.0
        print("📊 Call statistics reset")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_session()
