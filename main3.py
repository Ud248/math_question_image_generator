import asyncio
from llm.local_search import DeepSeekService
from llm.prompt_templates import EXTRACT_DATA_DRAW_COLUMN_CALC_PROMPT
from drawings.draw_column_calc import draw_column_calc_with_json_input
from utils.parse_json_response import parse_json_response

async def main():
    TYPE_EXERCISE = "Tính"
    QUESTION = "Chọn phép đặt tính rồi tính đúng? (10đ). Đáp án: D"
    DETAIL ="""   
    Hình ảnh phép tính:
    Hình A: Viết số hạng thứ 1 là 24 678 ở hàng trên, số hạng thứ 2 là 4 viết hàng dưới thẳng hàng với số 2 ở hàng chục nghìn của số hạng thứ 1. Dấu x ở giữa. Dấu kẻ ngang dưới số hạng thứ 2. Kết quả là 98 712.
    Hình B: Viết số hạng thứ 1 là 24 678 ở hàng trên, số hạng thứ 2 là 4 viết hàng dưới thẳng hàng với số 6 ở hàng trăm của số hạng thứ 1. Dấu x ở giữa. Dấu kẻ ngang dưới số 4. Kết quả là 98 712.
    Hình C: Viết số hạng thứ 1 là 24 678 ở hàng trên, số hạng thứ 2 là 4 viết hàng dưới thẳng hàng với số 7 ở hàng chục của số hạng thứ 1. Dấu x ở giữa. Dấu kẻ ngang dưới số 4. Kết quả là 98 712.
    Hình D: Viết số hạng thứ 1 là 24 678 ở hàng trên, số hạng thứ 2 là 4 viết hàng dưới thẳng hàng với số 8 ở hàng đơn của số hạng thứ 1. Dấu x ở giữa. Dấu kẻ ngang dưới số 4. Kết quả là 98 712.
    """
    prompt = EXTRACT_DATA_DRAW_COLUMN_CALC_PROMPT.format(
        type_exercise=TYPE_EXERCISE,
        question=QUESTION,
        detail=DETAIL
    )

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
            draw_column_calc_with_json_input(parsed, output_file='column_calc_output.png')
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