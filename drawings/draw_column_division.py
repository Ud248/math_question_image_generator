import matplotlib.pyplot as plt
import sys
import json
import os

sys.path.insert(0, '..')
from utils.merge_images import merge_images

def draw_column_division(dividend, divisor, quotient, step_offsets, remainder=None, title="",
                      figsize=(10, 8), start_row=8, start_col=1, filename="single_column_division_output.png"):
    """
    Vẽ phép chia cột theo phong cách sách giáo khoa Tiểu học Việt Nam.

    Các tham số:
    -----------
    dividend : str
        Số bị chia (ví dụ: "34568")
    divisor : str
        Số chia (ví dụ: "6")
    quotient : str
        Thương (ví dụ: "5761")
    step_offsets : list of tuple
        Danh sách các bước chia trung gian kèm vị trí lệch
        Mỗi phần tử là một tuple (giá trị, vị trí lệch)
        Ví dụ: [("45", 1), ("36", 2), ("08", 3), ("2", 4)]
        offset: số âm = lệch trái, số dương = lệch phải, 0 = thẳng hàng
    remainder : str, optional
        Số dư (nếu có)
    title : str
        Tiêu đề
    figsize : tuple
        Kích thước hình vẽ
    start_row : int
        Dòng bắt đầu (tính từ dưới lên)
    start_col : int
        Cột bắt đầu

    Trả về:
    -------
    filename: str
        Tên file hình ảnh đã lưu
    """
    
    # Set up figure and axes
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # Grid cell size - adjusted for 0.3 spacing
    cell_size = 0.3
    grid_width = max(10, (len(dividend) + len(divisor) + len(remainder) + len(quotient) + 2) * cell_size)
    grid_height = max(10, start_row + 3)
    
    # 1. Write dividend (top row, left side)
    for i, digit in enumerate(dividend):
        ax.text(start_col + i * cell_size + cell_size/2, start_row + 0.5, digit, 
                fontsize=20, ha='center', va='center', fontweight='bold')

    # 2. Draw vertical divider line (after dividend)
    divider_col = start_col + len(dividend) * cell_size + cell_size
    ax.plot([divider_col, divider_col], [start_row - 1, start_row + 1], 
            color='black', linewidth=2)
    
    # 3. Write divisor (same row as dividend, after vertical line)
    divisor_col = divider_col + cell_size/2
    ax.text(divisor_col + cell_size/2, start_row + 0.5, divisor, 
            fontsize=20, ha='left', va='center', fontweight='bold')
    
    # 4. Draw horizontal line (below divisor, above quotient, length of quotient)
    horizontal_line_y = start_row
    horizontal_line_x_start = divider_col
    horizontal_line_x_end = divisor_col + len(quotient) * cell_size
    ax.plot([horizontal_line_x_start, horizontal_line_x_end], 
            [horizontal_line_y, horizontal_line_y], 
            color='black', linewidth=2)
    
    # 5. Write quotient (below horizontal line)
    for i, digit in enumerate(quotient):
        ax.text(divisor_col + i * cell_size + cell_size/2, start_row - 0.5, digit, 
                fontsize=20, ha='left', va='center', fontweight='bold')
    
    # 6. Write intermediate division steps (left of divider line, below dividend)
    for idx, (step, offset) in enumerate(step_offsets):
        row = start_row - 1 - idx  # Go down from dividend
        # Calculate position based on offset from first digit of dividend
        col_start = start_col + offset * cell_size
        for i, digit in enumerate(step):
            ax.text(col_start + i * cell_size + cell_size/2, row + 0.5, digit, 
                    fontsize=20, ha='center', va='center', fontweight='bold')
    
    # 7. Write complete result at the bottom
    if remainder and remainder != '0':
        # Add space for dividend if larger than 3 digits
        if len(dividend) > 3:
            dividend_format = f"{dividend[0:2]} {dividend[2:]}"
        else:
            dividend_format = dividend
        result = f"{dividend_format} : {divisor} = {quotient} (dư {remainder})"
    else:
        result = f"{dividend} : {divisor} = {quotient}"
    
    # Tính vị trí y của result: cách bước chia cuối cùng 1.5 ô
    last_step_row = start_row - 1 - len(step_offsets)
    result_y = last_step_row - 1.5
    
    ax.text(start_col + cell_size/2, result_y, result, 
            fontsize=20, ha='left', va='center', 
            fontweight='bold')
    
    # Add title if provided
    if title:
        ax.text(start_col + cell_size/2, grid_height - 0.5, title, 
                fontsize=24, ha='center', va='top', fontweight='bold')
    
    # Set up axes
    ax.set_xlim(0, grid_width)
    ax.set_ylim(0, grid_height)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    
    plt.savefig(filename, dpi=300)
    return filename

def draw_column_division_with_json_input(json_input, output_file='column_division_output.png'):
    """
    Đọc spec từ file JSON (list item có keys: 'dividend', 'divisor', 'quotient', 'step_offsets', 'remainder', 'title')
    Tạo các column division theo vị trí trong list, ghép thành 1 ảnh và lưu output_file
    """
    # Nếu nhận list/tuple thì dùng trực tiếp, nếu là đường dẫn thì mở file
    if isinstance(json_input, (list, tuple)):
        specs = json_input
    elif isinstance(json_input, (str, bytes, bytearray, os.PathLike)):
        with open(json_input, "r", encoding="utf-8") as f:
            specs = json.load(f)

    images = []
    for idx, spec in enumerate(specs):
        dividend = spec.get('dividend', '')
        divisor = spec.get('divisor', '')
        quotient = spec.get('quotient', '')
        step_offsets = spec.get('step_offsets', [])
        remainder = spec.get('remainder', None)
        title = spec.get('title', '')

        temp_filename = f"temp_division_{idx}.png"
        draw_column_division(
            dividend=dividend,
            divisor=divisor,
            quotient=quotient,
            step_offsets=step_offsets,
            remainder=remainder,
            title=title,
            filename=temp_filename
        )
        images.append(temp_filename)

    # Ghép các ảnh lại với nhau
    if images:
        merge_images(images, output_filename=output_file, direction="horizontal")
        for img in images:
            if os.path.exists(img):
                os.remove(img)
        print(f"✅ Đã lưu hình ảnh: {output_file}")
    else:
        print("❌ Không có ảnh để ghép.")

if __name__ == "__main__":
    # Example 1: 34568 : 6 = 5761 (remainder 2)
    draw_column_division(
        dividend="34568",
        divisor="6",
        quotient="5761",
        step_offsets=[
            ("45", 1),
            ("36", 2),
            ("08", 3),
            ("2", 4)
        ],
        remainder="2",
        title="A.",
        filename="long_division_example1.png"
    )

    # Example 2: 178675 : 5 = 35732
    draw_column_division(
        dividend="178675",
        divisor="5",
        quotient="35732",
        step_offsets=[
            ("28", 1),
            ("36", 2),
            ("17", 3),
            ("25", 4),
            ("0", 5)
        ],
        remainder="5",
        title="B.",
        filename="long_division_example2.png"
    )

    # Example 3: 77965 : 6 = 12995 (dư 25)
    draw_column_division(
        dividend="77965",
        divisor="6",
        quotient="1299",
        step_offsets=[
            ("17", 0),
            ("59", 1),
            ("56", 2),
            ("25", 3)
        ],
        remainder="25",
        title="C.",
        filename="long_division_example3.png"
    )

    merge_images(output_filename='final_output.png',
                image_files=["long_division_example1.png", "long_division_example2.png", "long_division_example3.png"],
                direction="horizontal")

    # Example: 123456789012345 : 23 = 5367686478797 (remainder 4)
    draw_column_division(
        dividend="123456789012345",
        divisor="23",
        quotient="5367686478797",
        step_offsets=[
            ("12", 0),
            ("03", 1),
            ("34", 2),
            ("115", 3),
            ("66", 4),
            ("65", 5),
            ("57", 6),
            ("58", 7),
            ("59", 8),
            ("70", 9),
            ("71", 10),
            ("02", 11),
            ("23", 12),
            ("24", 13),
            ("15", 14)
        ],
        remainder="4",
        filename="long_division_example5.png",
    )