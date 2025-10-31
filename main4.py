import asyncio
from llm.local_search import DeepSeekService
from llm.prompt_templates import EXTRACT_DATA_DRAW_COLUMN_DIVISION_PROMPT
from drawings.draw_column_division import draw_column_division_with_json_input
from utils.parse_json_response import parse_json_response

async def main():
    TYPE_EXERCISE = "Tính"
    QUESTION = "(10đ) Phép chia nào sai. Đáp án: C"
    DETAIL ="""   
    Hình ảnh A: Đặt tính phép chia số bị chia 34 568 và số chia là 6. Thương là 5 761
    Ta viết số bị chia 34 568 tiếp theo kẻ 1 đường kẻ dọc và 1 đường kẻ ngang chia ô số chia và ô thương. Viết 6 vào ô số chia; viết 5 761 vào ô thương
    Ô số bị chia: dòng 1: viết “34 568”, dòng 2 viết số 45 thẳng hàng với số 4 và số 5 ở số bị chia. dòng 3: số 36 thẳng hàng với chữ số 56 của số bị chia; dòng 4 số 08 thẳng hàng với chữ số 68 của số bị chia. dòng 5: số 2 thẳng hàng với chữ số 8 của số bị chia
    Dòng 6: 34 568 : 6 = 5 761 (dư 2)

    Hình ảnh B: Đặt tính phép chia số bị chia 178 675 và số chia là 5. Thương là 35 735
    Ta viết số bị chia 178 675 tiếp theo kẻ 1 đường kẻ dọc và 1 đường kẻ ngang chia ô số chia và ô thương. Viết 5 vào ô số chia; viết 35 735 vào ô thương.
    Ô số bị chia:

    Dòng 1: viết "178 675"
    Dòng 2: viết số 28 thẳng hàng với số 7 và số 8 ở số bị chia
    Dòng 3: số 36 thẳng hàng với chữ số 86 của số bị chia
    Dòng 4: số 17 thẳng hàng với chữ số 67 của số bị chia
    Dòng 5: số 25 thẳng hàng với chữ số 75 của số bị chia
    Dòng 6: số 0 thẳng hàng với chữ số 5 của số bị chia

    Dòng 7: 178 675 : 5 = 35 735

    Hình ảnh C: Đặt tính phép chia số bị chia 77 965 và số chia là 6. Thương là 1 299
    Ta viết số bị chia 77 965 tiếp theo kẻ 1 đường kẻ dọc và 1 đường kẻ ngang chia ô số chia và ô thương. Viết 6 vào ô số chia; viết 1 299 vào ô thương.
    Ô số bị chia:

    Dòng 1: viết "77 965"
    Dòng 2: viết số 17 thẳng hàng với số 7 và số 7 ở số bị chia
    Dòng 3: số 59 thẳng hàng với chữ số 79 của số bị chia
    Dòng 4: số 56 thẳng hàng với chữ số 96 của số bị chia
    Dòng 5: số 25 thẳng hàng với chữ số 65 của số bị chia

    Dòng 6: 77 965 : 6 = 1 299 (dư 25)
    """
    prompt = EXTRACT_DATA_DRAW_COLUMN_DIVISION_PROMPT.format(
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
            draw_column_division_with_json_input(parsed, output_file='column_division_output.png')
        else:
            print(response)
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    finally:
        await service.close_session()
        print("\n✅ Session closed")

if __name__ == "__main__":
    asyncio.run(main())