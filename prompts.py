EXTRACT_DATA_DRAW_CIRCLE_PROMPT = """
Dựa trên 3 đoạn văn bản sau:

Loại bài: {type_exercise}

Tên bài học: {unit}

Mô tả hình vẽ: {detail}

Hãy phân tích nội dung và trích xuất thông tin về tất cả các hình tròn cần vẽ (có thể là 1 hoặc nhiều hình tròn). 
Kết quả trả về dưới dạng một mảng JSON, trong đó mỗi hình tròn sẽ được biểu diễn dưới dạng một object với các trường sau:

number(int, bắt buộc): Số cần hiển thị trong hình tròn. Nếu không có số, đặt giá trị là null.

order(mảng các int, bắt buộc): Vị trí của hình tròn trong ảnh ghép. Vị trí bắt đầu từ 0.

color(string, bắt buộc): Màu sắc Tiếng Anh của hình tròn.

Yêu cầu:
Cả 3 trường number, order, color đều là bắt buộc cho mỗi hình tròn. Nếu không có số, đặt giá trị là null. Nếu đề bài không ghi rõ, hãy suy luận hơp lý dựa trên ngữ cảnh. Màu sắc nên là các màu cơ bản tone tối.

Chỉ trả về một mảng JSON hợp lệ, không kèm giải thích, văn bản hay bình luận.

Ví dụ đầu ra mong muốn:
[
    {{
        "number": "1",
        "order": [0, 3, 9],
        "color": "blue"
    }},
    {{
        "number": "2",
        "order": [1, 7, 10],
        "color": "green"
    }},
    {{
        "number": "3",
        "order": [2, 5, 8],
        "color": "purple"
    }},
    {{
        "number": null,
        "order": [4, 6, 11],
        "color": "red"
    }}
]
"""