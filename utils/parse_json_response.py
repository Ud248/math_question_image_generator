import json
import re

def parse_json_response(response: str):
    """
    Parse JSON response từ LLM, tự động fix các lỗi format thường gặp
    
    Args:
        response: Raw response từ LLM
        
    Returns:
        dict hoặc list: Parsed JSON data
    """
    response = response.strip()
    
    # Case 1: Response là array hợp lệ [...]
    if response.startswith('[') and response.endswith(']'):
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            return None
    
    # Case 2: Response là object hợp lệ {...}
    if response.startswith('{') and response.endswith('}'):
        try:
            parsed = json.loads(response)
            # Nếu parse thành công và là dict đơn lẻ, return luôn
            return parsed
        except json.JSONDecodeError:
            pass
    
    # Case 3: Response có nhiều objects nhưng thiếu dấu [ ]
    # Ví dụ: {...}, {...}, {...}
    if response.startswith('{'):
        try:
            # Thêm dấu [ ] bao ngoài
            fixed_response = '[' + response + ']'
            print("🔧 Auto-fixed: Added [ ] wrapper around objects")
            return json.loads(fixed_response)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error after fix: {e}")
            return None
    
    # Case 4: Response có markdown code block ```json ... ```
    json_match = re.search(r'```(?:json)?\s*(\[.*?\]|\{.*?\})\s*```', response, re.DOTALL)
    if json_match:
        try:
            print("🔧 Auto-fixed: Extracted from markdown code block")
            return json.loads(json_match.group(1))
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            return None
    
    print("❌ Cannot parse JSON response")
    return None
