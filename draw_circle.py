from PIL import Image, ImageDraw, ImageFont, ImageColor

import json


def draw_circle_with_number(radius, number=None, color=(100, 149, 237, 255), font_path=None):
    """Vẽ 1 hình tròn có thể có hoặc không có số ở giữa (nền trong suốt + căn giữa chuẩn)"""
    size = radius * 2 + 10
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = (size // 2, size // 2)

    # Vẽ hình tròn
    draw.ellipse(
        [(center[0] - radius, center[1] - radius),
         (center[0] + radius, center[1] + radius)],
        fill=color
    )

    if number is not None:
        # --- Chọn font ---
        font_size = int(radius * 2)
        if font_path is None:
            # fallback thông minh
            import os
            candidates = [
                "fonts/Roboto/Roboto-VariableFont_wdth,wght.ttf"
            ]
            for path in candidates:
                if os.path.exists(path):
                    font_path = path
                    break

        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        text = str(number)

        # --- Lấy bbox thật của chữ ---
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # --- Tính vị trí chính giữa (dựa theo bbox thật) ---
        text_x = center[0] - text_w / 2
        text_y = center[1] - text_h / 2 - bbox[1]  # trừ bbox[1] để loại bỏ phần đệm baseline

        # --- Vẽ chữ ---
        draw.text((text_x, text_y), text, font=font, fill="white")

    return img



def combine_circles(circles, spacing=20):
    """Ghép danh sách hình tròn theo hàng ngang"""
    total_width = sum(im.width for im in circles) + spacing * (len(circles) - 1)
    max_height = max(im.height for im in circles)
    combined = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x_offset = 0
    for im in circles:
        combined.paste(im, (x_offset, 0), im)
        x_offset += im.width + spacing
    return combined

def draw_circles_with_json_input(json_input, output_file='circles_output.png', radius_default=40, spacing=0, font_path=None):
    """
    Đọc spec từ file JSON (list item có keys: 'text', 'order', 'color', optional 'radius')
    Tạo các circle theo vị trí trong 'order', ghép thành 1 ảnh và lưu output_file.

    Args:
        json_input_path (str): đường dẫn tới file JSON
        output_file (str): tên file output (png)
        radius_default (int): bán kính mặc định khi item không có 'radius'
        spacing (int): khoảng cách giữa các circle khi ghép
        font_path (str): đường dẫn font .ttf (tùy chọn)

    Returns:
        str: path file đã lưu
    """
    # Nếu nhận list/tuple thì dùng trực tiếp, nếu là đường dẫn thì mở file
    if isinstance(json_input, (list, tuple)):
        spec = json_input
    elif isinstance(json_input, (str, bytes, bytearray, os.PathLike)):
        with open(json_input, "r", encoding="utf-8") as f:
            spec = json.load(f)

    # Tìm tổng số slot bằng max order index
    max_idx = -1
    for item in spec:
        for pos in item.get('order', []):
            if isinstance(pos, int) and pos > max_idx:
                max_idx = pos
    total_slots = max_idx + 1 if max_idx >= 0 else 0
    if total_slots == 0:
        raise ValueError("Không tìm thấy trường 'order' hợp lệ trong JSON.")

    arranged = [None] * total_slots

    # Tạo và đặt ảnh theo order
    for item in spec:
        number = item.get('number', None)  # null -> None
        # nếu number is None thì draw_circle_with_number sẽ không vẽ chữ
        radius = item.get('radius', radius_default)
        # normalize color -> ImageColor.getrgb trả về RGB tuple
        try:
            rgb = ImageColor.getrgb(item.get('color', '#6495ED'))
            rgba = (*rgb, 255)
        except Exception:
            rgba = (100, 149, 237, 255)

        img = draw_circle_with_number(radius, number=number, color=rgba, font_path=font_path)

        for pos in item.get('order', []):
            if 0 <= pos < total_slots:
                arranged[pos] = img

    # placeholder transparent nếu còn slot chưa lấp
    placeholder = Image.new("RGBA", (radius_default * 2 + 10, radius_default * 2 + 10), (0, 0, 0, 0))
    for i in range(total_slots):
        if arranged[i] is None:
            arranged[i] = placeholder.copy()

    combined = combine_circles(arranged, spacing=spacing)
    combined.save(output_file)
    print(f"Saved: {output_file}")
    return output_file


# --- Demo ---
if __name__ == "__main__":
    # # Tạo các hình tròn
    # circles_1 = [draw_circle_with_number(40, 1, color=(255, 100, 100)) for _ in range(2)]
    # circles_2 = [draw_circle_with_number(40, 2, color=(100, 200, 100)) for _ in range(2)]
    # circles_none = [draw_circle_with_number(40, None, color=(150, 150, 255)) for _ in range(2)]

    # # Gom tất cả thành 1 danh sách
    # all_circles = circles_1 + circles_2 + circles_none  # total 6

    # # Mapping thứ tự mong muốn
    # order = {
    #     "1": [0, 3],
    #     "2": [1, 4],
    #     "none": [2, 5]
    # }

    # # Tạo danh sách sắp xếp theo mapping
    # arranged = [None] * 6
    # idx = 0
    # for key, positions in order.items():
    #     if key == "1":
    #         group = circles_1
    #     elif key == "2":
    #         group = circles_2
    #     else:
    #         group = circles_none

    #     for i, pos in enumerate(positions):
    #         arranged[pos] = group[i]

    # # Ghép lại thành 1 ảnh
    # combined = combine_circles(arranged, spacing=0)
    # combined.show()
    # combined.save("combine_circles.png")
    draw_circles_with_json_input("./data.json", output_file='circles_output.png')