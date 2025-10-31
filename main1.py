import asyncio
import json
from llm.local_search import DeepSeekService
from llm.prompt_templates import EXTRACT_DATA_DRAW_ANGLE_PROMPT
from drawings.draw_angle_func import draw_angles_from_json
from utils.parse_json_response import parse_json_response

async def main():
    """Interactive mode - sử dụng đề bài và mô tả constant"""
    
    DE_BAI = """
    "Số đo của góc đỉnh O, cạnh OA, OB là: 
    A. 120°
    B. 130°
    C. 145°
    D. 150°"
    """
    
    MO_TA = """
    Vẽ góc AOB, 
    Tia OA, OB màu xanh dương
    Chữ A, O, B màu tím
    Độ lớn góc: 90°
    Có vẽ cung tròn biểu diễn độ lớn góc

    Vẽ góc XYZ, 
    Tia ZY, XZ màu xanh dương
    Chữ X, Y, Z màu tím
    Độ lớn góc: 30
    Không vẽ cung tròn biểu diễn độ lớn góc
    """
    
    # Tạo prompt
    prompt = EXTRACT_DATA_DRAW_ANGLE_PROMPT.format(de_bai=DE_BAI.strip(), mo_ta=MO_TA.strip())
    
    service = DeepSeekService()
    
    print("\n" + "=" * 60)
    print("🤖 DeepSeek Interactive Mode")
    print("=" * 60)
    
    json_mode = True  # Mặc định bật JSON mode
    
    try:
        print(f"\n📝 JSON Mode: {'ON' if json_mode else 'OFF'}")
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