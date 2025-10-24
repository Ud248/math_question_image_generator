import asyncio
import json
import re
from local_search import DeepSeekService
from draw_angle_func import draw_angle, draw_multiple_angles

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

def create_prompt(de_bai: str, mo_ta: str) -> str:
    """
    Tạo prompt từ đề bài và mô tả
    
    Args:
        de_bai: Đề bài từ user
        mo_ta: Mô tả đề bài từ user
        
    Returns:
        str: Prompt hoàn chỉnh
    """
    return f"""
Dựa trên 2 đoạn văn bản sau:
Đề bài: 
{de_bai}

Mô tả đề bài:
{mo_ta}

Hãy phân tích nội dung và trích xuất thông tin về tất cả các góc cần vẽ (có thể là 1 hoặc nhiều góc).
Kết quả trả về dưới dạng một mảng JSON, trong đó mỗi phần tử là một góc với các trường sau:

angle_deg (float, bắt buộc): Góc cần vẽ (đơn vị độ). Ví dụ: 50, 120.

vertex_name (string, tùy chọn): Tên đỉnh của góc. Ví dụ: "O", "A", "V".

ray1_name (string, tùy chọn): Tên điểm trên tia thứ nhất. Ví dụ: "A", "B".

ray2_name (string, tùy chọn): Tên điểm trên tia thứ hai. Ví dụ: "B", "C".

ray1_color (string, tùy chọn): Màu của tia thứ nhất. Ví dụ: "blue", "red", "#FF5733".

ray2_color (string, tùy chọn): Màu của tia thứ hai. Ví dụ: "green", "orange", "#33FF57".

vertex_label_color (string, tùy chọn): Màu của nhãn đỉnh. Ví dụ: "black", "purple", "#000000".

Yêu cầu:

angle_deg là bắt buộc cho mỗi góc. Nếu đề bài không ghi rõ, hãy suy luận hợp lý dựa trên ngữ cảnh.

Các trường khác có thể để null nếu không có thông tin.

Chỉ trả về một mảng JSON hợp lệ, không kèm giải thích, văn bản hay bình luận.

Ví dụ đầu ra mong muốn:

[
  {{
    "angle_deg": 50,
    "vertex_name": "O",
    "ray1_name": "A",
    "ray2_name": "B",
    "ray1_color": "blue",
    "ray2_color": "red",
    "vertex_label_color": "purple"
  }},
  {{
    "angle_deg": 120,
    "vertex_name": "A",
    "ray1_name": "M",
    "ray2_name": "N",
    "ray1_color": null,
    "ray2_color": null,
    "vertex_label_color": null
  }}
]
"""

def normalize_angles_data(data):
    """
    Chuẩn hóa dữ liệu từ LLM thành list of dict
    
    Args:
        data: Có thể là dict (1 góc) hoặc list of dict (nhiều góc)
        
    Returns:
        list: Luôn trả về list of dict
    """
    # Nếu là dict đơn lẻ -> chuyển thành list có 1 phần tử
    if isinstance(data, dict):
        print("📦 Normalized: Single dict → List with 1 element")
        return [data]
    
    # Nếu đã là list -> giữ nguyên
    elif isinstance(data, list):
        print(f"📦 Normalized: Already a list with {len(data)} element(s)")
        return data
    
    # Trường hợp khác -> trả về list rỗng
    else:
        print("⚠️ Warning: Invalid data type, returning empty list")
        return []

def draw_angles_from_json(angles_data):
    """
    Vẽ góc dựa trên dữ liệu JSON từ LLM
    
    Args:
        angles_data: Dict (1 góc) hoặc List of dict (nhiều góc)
    """
    # ✅ Chuẩn hóa data thành list
    angles_list = normalize_angles_data(angles_data)
    
    if not angles_list:
        print("❌ No valid angle data to draw")
        return
    
    print(f"\n🎨 Drawing {len(angles_list)} angle(s)...")
    print("=" * 60)
    
    if len(angles_list) == 1:
        # Vẽ 1 góc - dùng draw_angle
        angle_info = angles_list[0]
        print(f"📐 Drawing single angle: {angle_info.get('angle_deg', 'Unknown')}°")
        
        try:
            fig = draw_angle(
                angle_deg=angle_info.get('angle_deg'),
                vertex_name=angle_info.get('vertex_name'),
                ray1_name=angle_info.get('ray1_name'),
                ray2_name=angle_info.get('ray2_name'),
                vertex_label_color=angle_info.get('vertex_label_color'),
                ray1_color=angle_info.get('ray1_color'),
                ray2_color=angle_info.get('ray2_color')
            )
            print("✅ Single angle drawn successfully!")
            return fig
        except Exception as e:
            print(f"❌ Error drawing single angle: {e}")
            return None
    
    else:
        # Vẽ nhiều góc - dùng draw_multiple_angles
        print(f"📐 Drawing multiple angles:")
        for i, angle_info in enumerate(angles_list, 1):
            print(f"  {i}. Angle: {angle_info.get('angle_deg', 'Unknown')}° "
                  f"(Vertex: {angle_info.get('vertex_name', 'N/A')})")
        
        try:
            fig = draw_multiple_angles(angles_list)
            print("✅ Multiple angles drawn successfully!")
            return fig
        except Exception as e:
            print(f"❌ Error drawing multiple angles: {e}")
            return None

async def main():
    """Interactive mode - sử dụng đề bài và mô tả constant"""
    
    DE_BAI = """
"Cạnh IT đi qua điểm số mấy để tạo được góc 90°? 
A. Điểm số 1
B. Điểm số 2
C. Điểm số 3
D. Không đi qua điểm nào"
    """
    
    MO_TA = """
"Vẽ thước đo góc nửa hình tròn đặt trùng với cạnh thẳng trên đường thẳng MI màu tím; tâm thước đúng tại I (M ở bên trái).
Trên cung thước có ba dấu chấm hồng được đánh số:
Ở phía trái, gần vạch 20°.
Ở đỉnh trên đúng vạch 90° (đường thẳng đứng qua I).
Ở phía phải, vạch 120°.
Các vạch chia 0°–180° hiện rõ trên mép thước."
    """
    
    # Tạo prompt
    prompt = create_prompt(DE_BAI.strip(), MO_TA.strip())
    
    service = DeepSeekService()
    
    print("\n" + "=" * 60)
    print("🤖 DeepSeek Interactive Mode")
    print("=" * 60)
    
    json_mode = True  # Mặc định bật JSON mode
    
    try:
        print(f"\n📝 JSON Mode: {'ON' if json_mode else 'OFF'}")
        print(f"\n💬 Generated Prompt:")
        print("-" * 60)
        print(f"Đề bài: {DE_BAI.strip()}")
        print(f"Mô tả: {MO_TA.strip()}")
        print("-" * 60)
        
        print("\n⏳ Generating response from LLM...")
        response = await service.generate_message(prompt, is_json_mode=json_mode)
        
        print("\n" + "=" * 60)
        print("🤖 LLM Response:")
        print("-" * 60)
        
        if json_mode:
            # ✅ Parse JSON với auto-fix
            parsed = parse_json_response(response)
            
            if parsed is None:
                print(f"❌ Invalid JSON - Cannot parse")
                print(f"Raw response: {response}")
                return
            
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
            
            # ✅ Vẽ góc dựa trên JSON response (tự động xử lý dict hoặc list)
            print("\n" + "=" * 60)
            draw_angles_from_json(parsed)
        else:
            print(response)
        
        print("=" * 60)
        
        # Print statistics
        print("\n📊 Call Statistics")
        print("-" * 60)
        stats = service.get_call_stats()
        print(f"Total calls: {stats['total_calls']}")
        print(f"Total time: {stats['total_time']:.2f}s")
        print(f"Average duration: {stats['average_duration']:.2f}s")
        print(f"Model: {stats['model']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    finally:
        await service.close_session()
        print("\n✅ Session closed")

if __name__ == "__main__":
    asyncio.run(main())