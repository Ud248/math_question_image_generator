EXTRACT_DATA_DRAW_ANGLE_PROMPT = """
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

angle_deg là bắt buộc cho mỗi góc. Nếu đề bài không ghi rõ, hãy suy luận hợp lý dựa trên ngữ cảnh. Nếu có tên đỉnh và các tia, hãy tự bổ sung màu sắc mặc định (ví dụ: tia 1 màu xanh, tia 2 màu đỏ, nhãn đỉnh màu đen) nếu không có thông tin cụ thể.

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