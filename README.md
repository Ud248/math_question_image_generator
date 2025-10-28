# 📐 Angel Generator - Trình Tạo Hình Ảnh Toán Học

Dự án tạo tự động hình ảnh minh họa cho bài tập toán học (góc, hình tròn) bằng cách sử dụng AI/LLM để phân tích đề bài và tạo hình vẽ tương ứng.

## 🎯 Tính Năng

- ✅ **Vẽ góc tự động**: Phân tích đề bài và tự động vẽ các góc với màu sắc, nhãn tùy chỉnh
- ✅ **Vẽ hình tròn với số**: Tạo các hình tròn có số ở giữa theo thứ tự chỉ định
- ✅ **Tích hợp LLM**: Sử dụng DeepSeek API để trích xuất thông tin từ đề bài
- ✅ **JSON Mode**: Tự động parse và xử lý kết quả JSON từ LLM
- ✅ **Customizable**: Tùy chỉnh màu sắc, kích thước, font chữ

## 📋 Yêu Cầu Hệ Thống

- Python 3.7+
- pip (Python package manager)

## 🚀 Cài Đặt

### 1. Clone hoặc tải dự án về máy

```bash
git clone <repository-url>
cd angel_generator
```

### 2. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

Các thư viện bao gồm:
- `matplotlib` - Vẽ đồ thị góc
- `numpy` - Tính toán toán học
- `openai` - Tích hợp với DeepSeek API
- `fastapi` - Framework web (nếu cần API)
- `aiohttp` - HTTP client bất đồng bộ
- `python-dotenv` - Quản lý biến môi trường
- `Pillow` - Xử lý hình ảnh (cho vẽ hình tròn)

### 3. Cấu hình biến môi trường

Tạo file `.env` từ file mẫu:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin API của bạn:

```env
DEEPSEEK_BASE_URL=https://ark.ap-southeast.bytepluses.com/api/v3
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=your_model_name_here
```

## 📖 Hướng Dẫn Sử Dụng

### 1. Vẽ Góc (main.py)

Chương trình phân tích đề bài về góc và tự động vẽ hình minh họa:

```bash
python main.py
```

**Ví dụ input:**

```python
DE_BAI = """
Đây là góc:
A. Góc nhọn
B. Góc tù
C. Góc bẹt
D. Góc vuông
"""

MO_TA = """
Hình vẽ gồm hai tia chung gốc I màu hồng:
Tia IM nghiêng lên về bên trái (đầu mút M).
Tia IN nằm ngang sang phải (đầu mút N).
Vì vậy góc MIN là góc tù (lớn hơn 90° và nhỏ hơn 180°).
"""
```

**Output:**
- File ảnh `angle.png` chứa hình vẽ góc
- Console hiển thị JSON response từ LLM
- Thống kê thời gian và số lần gọi API

### 2. Vẽ Hình Tròn (main2.py)

Chương trình tạo các hình tròn có số theo thứ tự:

```bash
python main2.py
```

**Ví dụ input:**

```python
TYPE_EXERCISE = "Hoàn thành dãy số"
UNIT = "Các số 0, 1, 2, 3, 4, 5"
DETAIL = """
Tạo 2 hình tròn có số 1 ở chính giữa
Tạo 2 hình tròn có số 2 ở chính giữa
...
Thứ tự xuất hiện: [0, 5], [1, 11], ...
"""
```

**Output:**
- File ảnh `circles_output.png` chứa các hình tròn được sắp xếp

## 🏗️ Cấu Trúc Dự Án

```
angel_generator/
├── main.py                     # Script vẽ góc
├── main2.py                    # Script vẽ hình tròn
├── prompts.py                  # Template prompt cho LLM
├── requirements.txt            # Dependencies
├── .env.example               # Mẫu file cấu hình
├── fonts/                     # Thư mục font chữ
│   └── Roboto/               # Font Roboto
├── llm/                       # Module LLM
│   ├── __init__.py
│   └── local_search.py       # DeepSeek API service
└── utils/                     # Tiện ích
    ├── __init__.py
    ├── draw_angle_func.py    # Vẽ góc
    ├── draw_circle.py        # Vẽ hình tròn
    ├── normalize_angles_data.py  # Chuẩn hóa dữ liệu góc
    └── parse_json_response.py    # Parse JSON từ LLM
```

## 🔧 API Reference

### DeepSeekService

Lớp quản lý tương tác với DeepSeek LLM API.

```python
from llm.local_search import DeepSeekService

service = DeepSeekService()

# Tạo message với JSON mode
response = await service.generate_message(prompt, is_json_mode=True)

# Lấy thống kê
stats = service.get_call_stats()

# Đóng session
await service.close_session()
```

### draw_angle()

Vẽ góc với các tham số tùy chỉnh.

```python
from utils.draw_angle_func import draw_angle

draw_angle(
    angle_deg=50,              # Góc (độ)
    vertex_name='O',           # Tên đỉnh
    ray1_name='A',            # Tên điểm tia 1
    ray2_name='B',            # Tên điểm tia 2
    ray1_color='blue',        # Màu tia 1
    ray2_color='red',         # Màu tia 2
    vertex_label_color='black',  # Màu nhãn
    output_file='angle.png'   # File output
)
```

### draw_circles_with_json_input()

Vẽ nhiều hình tròn theo cấu hình JSON.

```python
from utils.draw_circle import draw_circles_with_json_input

json_data = [
    {
        "text": "1",
        "order": [0, 5],
        "color": "#6495ED"
    },
    {
        "text": None,  # Hình tròn trống
        "order": [2, 6],
        "color": "#6495ED"
    }
]

draw_circles_with_json_input(
    json_input=json_data,
    output_file='circles.png',
    radius_default=40,
    spacing=20
)
```

## 📝 Format JSON Response

### Cho vẽ góc:

```json
[
  {
    "angle_deg": 50,
    "vertex_name": "O",
    "ray1_name": "A",
    "ray2_name": "B",
    "ray1_color": "blue",
    "ray2_color": "red",
    "vertex_label_color": "purple"
  }
]
```

### Cho vẽ hình tròn:

```json
[
  {
    "text": "1",
    "order": [0, 5],
    "color": "#6495ED",
    "radius": 40
  }
]
```

## 🛠️ Tùy Chỉnh

### Thay đổi font chữ

Đặt font `.ttf` vào thư mục `fonts/` và chỉ định path khi gọi hàm:

```python
draw_circles_with_json_input(
    json_input=data,
    font_path='fonts/YourFont/YourFont.ttf'
)
```

### Tùy chỉnh màu sắc

Hỗ trợ nhiều định dạng màu:
- Tên màu: `'blue'`, `'red'`, `'green'`
- Hex code: `'#FF5733'`, `'#33FF57'`
- RGB/RGBA tuple: `(100, 149, 237, 255)`

### Điều chỉnh prompt

Chỉnh sửa file `prompts.py` để thay đổi cách LLM phân tích đề bài.

## ⚙️ Cấu Hình Nâng Cao

### DeepSeek API Settings

Trong file `llm/local_search.py`, bạn có thể điều chỉnh:

```python
self.timeout = 100.0          # Timeout (giây)
self.max_retries = 3          # Số lần retry
self.retry_delay = 1.0        # Delay giữa các retry
```

### Connection Pool (cho concurrent requests)

```python
connector = aiohttp.TCPConnector(
    limit=100,              # Tổng số kết nối
    limit_per_host=20,      # Kết nối tối đa/host
    ttl_dns_cache=300,      # DNS cache TTL
)
```

## 🐛 Xử Lý Lỗi

### Lỗi JSON parse

Hệ thống tự động sửa các lỗi JSON phổ biến:
- Thiếu dấu ngoặc
- Dấu phẩy thừa
- Markdown code blocks (`json`)

### Lỗi API

Tự động retry với exponential backoff khi:
- Timeout
- Network error
- Server error (5xx)

## 📊 Output Mẫu

### Console Output

```
============================================================
🤖 DeepSeek Interactive Mode
============================================================

📝 JSON Mode: ON

💬 Generated Prompt:
------------------------------------------------------------
Đề bài: Đây là góc: A. Góc nhọn...
Mô tả: Hình vẽ gồm hai tia chung gốc...
------------------------------------------------------------

⏳ Generating response from LLM...

============================================================
🤖 LLM Response:
------------------------------------------------------------
[
  {
    "angle_deg": 120,
    "vertex_name": "I",
    "ray1_name": "M",
    "ray2_name": "N",
    "ray1_color": "pink",
    "ray2_color": "pink",
    "vertex_label_color": "black"
  }
]
============================================================

📊 Call Statistics
------------------------------------------------------------
Total calls: 1
Total time: 2.34s
Average duration: 2.34s
Model: ep-20250429194234-4m2tz

✅ Session closed
```

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phát hành dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 📧 Liên Hệ

Nếu có câu hỏi hoặc đề xuất, vui lòng tạo issue trên GitHub.

## 🙏 Credits

- Font Roboto - Google Fonts
- DeepSeek API - BytePlus
- Matplotlib, NumPy, Pillow - Python libraries

---

Made with ❤️ for education