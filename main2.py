import asyncio
from llm.local_search import DeepSeekService
from utils.draw_circle import draw_circles_with_json_input
from utils.parse_json_response import parse_json_response
from prompts import EXTRACT_DATA_DRAW_CIRCLE_PROMPT

async def main():
    TYPE_EXERCISE = "Hoàn thành dãy số"
    UNIT = "Các số 0, 1, 2, 3, 4, 5"
    DETAIL ="""
    Điền số thích hợp vào chỗ trống
    Đáp án : Các số cần điền theo thứ tự từ trái qua phải là: 3, 2, 4, 1, 5

    Tạo 2 hình ảnh 1 hình tròn có số 1 ở chính giữa 
    Tạo 2 hình ảnh 1 hình tròn có số 2 ở chính giữa
    Tạo 2 hình ảnh 1 hình tròn có số 3 ở chính giữa
    Tạo 2 hình ảnh 1 hình tròn có số 4 ở chính giữa
    Tạo 2 hình ảnh 1 hình tròn có số 5 ở chính giữa
    Tạo 5 hình ảnh 1 hình tròn không in số
    Thứ tư xuất hiện của các hình tròn tính từ trái sang phải:
    - Hình tròn có số 1 ở chính giữa : [0, 5]
    - Hình tròn có số 2 ở chính giữa : [1, 11]
    - Hình tròn có số 3 ở chính giữa : [7, 12]
    - Hình tròn có số 4 ở chính giữa : [3, 13]
    - Hình tròn có số 5 ở chính giữa : [4, 9]
    - Hình tròn không có số ở chính giữa : [2, 6, 8, 10, 14]
    """
    prompt = EXTRACT_DATA_DRAW_CIRCLE_PROMPT.format(
        type_exercise=TYPE_EXERCISE,
        unit=UNIT,
        detail=DETAIL
    )

    service = DeepSeekService()

    print("\n" + "=" * 60)
    print("🤖 DeepSeek Interactive Mode")
    print("=" * 60)
    
    json_mode = True  # Mặc định bật JSON mode
    
    try:
        print(f"\n📝 JSON Mode: {'ON' if json_mode else 'OFF'}")
        print(f"\n💬 Generated Prompt:")
        print("-" * 60)
        print(f"Loại bài: {TYPE_EXERCISE.strip()}")
        print(f"Tên bài học: {UNIT.strip()}")
        print(f"Mô tả hình vẽ: {DETAIL.strip()}")
        print("-" * 60)
        
        print("\n⏳ Generating response from LLM...")
        response = await service.generate_message(prompt, is_json_mode=json_mode)
        
        print("\n" + "=" * 60)
        print("🤖 LLM Response:")
        print("-" * 60)
        
        print(response)
        if json_mode:
             # ✅ Parse JSON với auto-fix
            parsed = parse_json_response(response)
            
            if parsed is None:
                print(f"❌ Invalid JSON - Cannot parse")
                print(f"Raw response: {response}")
                return
            
            # ✅ Vẽ hình dựa trên JSON response (tự động xử lý dict hoặc list)
            print("\n" + "=" * 60)
            draw_circles_with_json_input(parsed, output_file='circles_output.png')
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