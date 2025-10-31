import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from utils.merge_images import merge_images
import os
import json

def draw_column_calc(num1, num2, operator, result, offset=0, 
                     title="", filename="calc.png", 
                     bg_style="white", font_size=24, line_gap=0.6, digit_spacing=0.2):
    """
    Vẽ phép tính đặt tính theo cột như trong vở học sinh
    
    Parameters:
    -----------
    num1 : str - Số thứ nhất
    num2 : str - Số thứ hai
    operator : str - Phép toán ('+', '-', '×')
    result : str - Kết quả
    offset : int - Độ lệch của num2 (âm=trái, dương=phải, 0=chuẩn)
    title : str - Tiêu đề
    filename : str - Tên file lưu
    bg_style : str - "white" hoặc "grid" (nền ô ly)
    font_size : int - Cỡ chữ
    line_gap : float - Khoảng cách dọc giữa các dòng
    digit_spacing : float - Khoảng cách giữa các chữ số (0.5-1.0)
    """
    
    # Hàm tính chiều rộng thực tế của số
    def calc_width(num_str):
        """Tính chiều rộng thực tế của số (có tính cả dấu phân cách)"""
        base_width = len(num_str) * digit_spacing
        return base_width
    
    # Hàm tính vị trí x cho từng chữ số
    def get_positions(num_str, end_x):
        """Trả về list vị trí x cho từng chữ số"""
        positions = []
        current_x = end_x
        
        # Duyệt từ phải sang trái
        for i in range(len(num_str) - 1, -1, -1):
            positions.append(current_x)
            current_x -= digit_spacing
        
        return positions[::-1]  # Đảo ngược lại
    
    # Tính toán kích thước
    max_width = max(calc_width(num1), calc_width(num2), calc_width(result))
    
    # Tạo figure
    fig_width = max(6, max_width * 0.6 + 2)
    fig_height = max(5, 5 * line_gap)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Thiết lập trục
    ax.set_xlim(-1.5, max_width + 1)
    ax.set_ylim(-1, 6)
    ax.axis('off')
    
    # Vẽ nền ô ly nếu cần
    if bg_style == "grid":
        grid_color = '#E8F4F8'
        cell_size = digit_spacing
        
        for i in range(int(-2/digit_spacing), int((max_width + 3)/digit_spacing) + 1):
            for j in range(-1, 7):
                rect = Rectangle((i * digit_spacing - digit_spacing/2, j - 0.5), 
                               cell_size, cell_size,
                               linewidth=0.5, edgecolor='#B8D4E0', 
                               facecolor=grid_color, alpha=0.5)
                ax.add_patch(rect)
    
    # Vị trí các dòng (điều chỉnh theo line_gap)
    y_title = 4.0 * (line_gap / 0.8) + 1.2
    y_num1 = 4.0 * (line_gap / 0.8)
    y_operator = 3.0 * (line_gap / 0.8)
    y_num2 = 2.0 * (line_gap / 0.8)
    y_line = 1.3 * (line_gap / 0.8)
    y_result = 0.5 * (line_gap / 0.8)
    
    # Vẽ tiêu đề
    ax.text(max_width / 2 - 2, y_title - 0.5, title, 
           fontsize=font_size * 0.8, ha='center', va='center',
           weight='bold', family='sans-serif')
    
    # Điểm căn phải (end point)
    x_end = max_width - 0.3
    
    # Vẽ num1
    positions1 = get_positions(num1, x_end)
    for pos, digit in zip(positions1, num1):
        ax.text(pos, y_num1, digit, 
               fontsize=font_size, ha='center', va='center',
               family='Times New Roman', weight='normal')
    
    # Vẽ dấu phép toán
    ax.text(-0.8, y_operator, operator, 
           fontsize=font_size, ha='center', va='center',
           family='Times New Roman', weight='normal')
    
    # Vẽ num2 (có offset)
    offset_distance = offset * digit_spacing
    positions2 = get_positions(num2, x_end + offset_distance)
    for pos, digit in zip(positions2, num2):
        ax.text(pos, y_num2, digit, 
               fontsize=font_size, ha='center', va='center',
               family='Times New Roman', weight='normal')
    
    # Vẽ đường kẻ ngang
    line_start_x = min(positions1[0], positions2[0]) - digit_spacing * 0.3
    line_end_x = max(positions1[-1], positions2[-1]) + digit_spacing * 0.3
    ax.plot([line_start_x, line_end_x], [y_line, y_line], 
           'k-', linewidth=2)
    
    # Vẽ kết quả
    positions_result = get_positions(result, x_end)
    for pos, digit in zip(positions_result, result):
        ax.text(pos, y_result, digit, 
               fontsize=font_size, ha='center', va='center',
               family='Times New Roman', weight='normal')
    
    # Lưu file
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', 
               facecolor='white' if bg_style == "white" else None)
    print(f"Đã lưu hình ảnh: {filename}")

def draw_column_calc_with_json_input(json_input, output_file='column_calc_output.png'):
    """
    Đọc spec từ file JSON (list item có keys: 'num1', 'num2', 'operator', 'result', 'offset', 'title')
    Tạo các column calculation theo vị trí trong list, ghép thành 1 ảnh và lưu output_file.
    """
    # Nếu nhận list/tuple thì dùng trực tiếp, nếu là đường dẫn thì mở file
    if isinstance(json_input, (list, tuple)):
        specs = json_input
    elif isinstance(json_input, (str, bytes, bytearray, os.PathLike)):
        with open(json_input, "r", encoding="utf-8") as f:
            specs = json.load(f)
    
    images = []
    for idx, spec in enumerate(specs):
        num1 = spec.get('num1', '')
        num2 = spec.get('num2', '')
        operator = spec.get('operator', '+')
        result = spec.get('result', '')
        offset = spec.get('offset', 0)
        title = spec.get('title', '')
        
        temp_filename = f"temp_calc_{idx}.png"
        draw_column_calc(num1, num2, operator, result, offset, title, temp_filename)
        images.append(temp_filename)
    
    # Ghép ảnh
    if images:
        merge_images(images, output_filename=output_file, direction="horizontal")
        # Xoá ảnh lẻ
        for temp_file in images:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        print(f"✅ Đã lưu ảnh tổng hợp: {output_file}")
    else:
        print("❌ Không có ảnh nào để ghép!")

# Ví dụ sử dụng
if __name__ == "__main__":
    draw_column_calc(num1="24678", num2="4", operator="×", result="98672", offset=-4, title="A.", filename="answer_A.png")
    draw_column_calc(num1="24678", num2="4", operator="×", result="98672", offset=-2, title="B.", filename="answer_B.png")
    draw_column_calc(num1="24678", num2="4", operator="×", result="98672", offset=-1, title="C.", filename="answer_C.png")
    draw_column_calc(num1="24678", num2="4", operator="×", result="98672", offset=-0, title="D.", filename="answer_D.png")

    merge_images(["answer_A.png", "answer_B.png", "answer_C.png", "answer_D.png"],output_filename="final_output.png", direction="horizontal")