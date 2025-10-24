"""
draw_angle.py
Vẽ ảnh minh họa góc đơn giản chỉ cần góc và tên các tia
Yêu cầu: matplotlib, numpy
"""
import matplotlib.pyplot as plt
import numpy as np
import math


def draw_angle(angle_deg, vertex_name='O', ray1_name='A', ray2_name='B', vertex_label_color='black',
               ray1_color='blue', ray2_color='red',output_file='angle.png'):
    """
    Vẽ góc đơn giản - chỉ cần góc và tên các tia

    Args:
        angle_deg (float): Góc cần vẽ (độ), ví dụ: 50, 120
        vertex_name (str): Tên đỉnh, ví dụ: 'O', 'A', 'V'
        ray1_name (str): Tên điểm trên tia thứ nhất, ví dụ: 'A', 'B'
        ray2_name (str): Tên điểm trên tia thứ hai, ví dụ: 'B', 'C',
        vertex_label_color (str): Màu nhãn đỉnh, ví dụ: 'black', 'purple', '#000000'
        ray1_color (str): Màu tia thứ nhất, ví dụ: 'blue', 'red', '#FF5733'
        ray2_color (str): Màu tia thứ hai, ví dụ: 'red', 'green', '#33FF57'
        output_file (str): Tên file output, ví dụ: 'angle.png'

    Returns:
        str: Đường dẫn file đã lưu

    Examples:
        >>> # Vẽ góc AOB = 50°
        >>> draw_angle(50, 'O', 'A', 'B')

        >>> # Vẽ góc XYZ = 120° với màu tùy chỉnh
        >>> draw_angle(120, 'Y', 'X', 'Z', 'purple', 'orange', 'angle_XYZ.png')
    """
    # Chuyển đổi sang radian
    angle_rad = math.radians(angle_deg)

    # Thiết lập độ dài tia và bán kính cung
    ray_length = 1.0
    arc_radius = 0.35

    # Định nghĩa các điểm
    vertex = np.array([0.0, 0.0])
    point1 = np.array([ray_length, 0.0])
    point2 = np.array([ray_length * math.cos(angle_rad),
                       ray_length * math.sin(angle_rad)])

    # Tạo figure
    fig, ax = plt.subplots(figsize=(5, 5))

    # Vẽ tia thứ nhất (từ vertex đến point1)
    ax.plot([vertex[0], point1[0]], [vertex[1], point1[1]],
            color=ray1_color, lw=2.5, label=f'Tia {vertex_name}{ray1_name}')

    # Vẽ tia thứ hai (từ vertex đến point2)
    ax.plot([vertex[0], point2[0]], [vertex[1], point2[1]],
            color=ray2_color, lw=2.5, label=f'Tia {vertex_name}{ray2_name}')

    # Vẽ các điểm
    ax.scatter([vertex[0]], [vertex[1]], s=40, c='black', zorder=5)
    ax.scatter([point1[0]], [point1[1]], s=40, c=ray1_color, zorder=5)
    ax.scatter([point2[0]], [point2[1]], s=40, c=ray2_color, zorder=5)

    # Đặt nhãn cho các điểm
    ax.text(point1[0] + 0.05, point1[1] - 0.05, ray1_name,
            fontsize=14, fontweight='bold', color=vertex_label_color)
    ax.text(vertex[0] - 0.08, vertex[1] - 0.08, vertex_name,
            fontsize=14, fontweight='bold', color=vertex_label_color)
    ax.text(point2[0] + 0.05, point2[1] + 0.03, ray2_name,
            fontsize=14, fontweight='bold', color=vertex_label_color)

    # Vẽ cung tròn biểu diễn góc
    theta = np.linspace(0, angle_rad, 120)
    ax.plot(arc_radius * np.cos(theta),
            arc_radius * np.sin(theta),
            color='green', lw=2.5)

    # Nhãn góc ở giữa cung
    mid_angle = angle_rad / 2
    label_x = arc_radius * math.cos(mid_angle) + 0.08
    label_y = arc_radius * math.sin(mid_angle) + 0.03
    ax.text(label_x, label_y, f"{angle_deg}°",
            fontsize=13, fontweight='bold', color='green',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='green', alpha=0.8))

    # Tính toán xlim và ylim dynamic dựa trên tất cả các điểm
    margin = 0.2
    all_x = [vertex[0], point1[0], point2[0]]
    all_y = [vertex[1], point1[1], point2[1]]
    
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    
    # Thêm margin cho đẹp
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)

    # Cài đặt hiển thị
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    # Lưu file
    fig.savefig(output_file, bbox_inches='tight', dpi=150, transparent=True)
    plt.close(fig)

    print(f"✓ Đã vẽ góc {vertex_name}{ray1_name}{ray2_name} = {angle_deg}°")
    print(f"✓ File: {output_file}")
    return output_file


def draw_multiple_angles(angles_data, output_prefix='angle'):
    """
    Vẽ nhiều góc cùng lúc

    Args:
        angles_data (list): List các dict chứa thông tin góc
            Mỗi dict có format:
            {
                'angle_deg': 50,
                'vertex_name': 'O',
                'ray1_name': 'A',
                'ray2_name': 'B',
                'ray1_color': 'blue',  # tùy chọn
                'ray2_color': 'red',   # tùy chọn
                'vertex_label_color': 'black'  # tùy chọn
            }
        output_prefix (str): Tiền tố tên file output

    Returns:
        list: Danh sách các file đã tạo

    Example:
        >>> angles = [
        ...     {'angle_deg': 50, 'vertex_name': 'O', 'ray1_name': 'A', 'ray2_name': 'B'},
        ...     {'angle_deg': 120, 'vertex_name': 'X', 'ray1_name': 'Y', 'ray2_name': 'Z',
        ...      'ray1_color': 'purple', 'ray2_color': 'orange'}
        ... ]
        >>> draw_multiple_angles(angles)
    """
    files = []
    for i, data in enumerate(angles_data):
        angle = data.get('angle_deg')
        vertex = data.get('vertex_name', 'O')
        ray1 = data.get('ray1_name', 'A')
        ray2 = data.get('ray2_name', 'B')
        color1 = data.get('ray1_color', 'blue')
        color2 = data.get('ray2_color', 'red')
        vertex_label_color = data.get('vertex_label_color', 'black')

        output_file = f"{output_prefix}_{vertex}{ray1}{ray2}_{angle}.png"

        draw_angle(angle, vertex, ray1, ray2, vertex_label_color, color1, color2, output_file)
        files.append(output_file)

    return files


# ==================== DEMO USAGE ====================
if __name__ == "__main__":
    print("=== Demo Vẽ Góc Đơn Giản ===\n")

    # Ví dụ 1: Vẽ góc AOB = 50° (cơ bản nhất)
    print("1. Vẽ góc AOB = 50°:")
    draw_angle(angle_deg=50)

    # Ví dụ 2: Vẽ góc XYZ = 120° với tên tùy chỉnh
    print("\n2. Vẽ góc XYZ = 120°:")
    draw_angle(
        angle_deg=120,
        vertex_name='Y',
        ray1_name='X',
        ray2_name='Z',
        output_file='angle_XYZ.png'
    )

    # Ví dụ 3: Vẽ góc với màu tùy chỉnh
    print("\n3. Vẽ góc MON = 75° với màu tùy chỉnh:")
    draw_angle(
        angle_deg=75,
        vertex_name='O',
        ray1_name='M',
        ray2_name='N',
        ray1_color='purple',
        ray2_color='orange',
        output_file='angle_MON.png'
    )

    # Ví dụ 4: Vẽ nhiều góc cùng lúc
    print("\n4. Vẽ nhiều góc cùng lúc:")
    angles = [
        {
            'angle': 30,
            'vertex': 'A',
            'ray1': 'B',
            'ray2': 'C',
            'color1': 'blue',
            'color2': 'red'
        },
        {
            'angle': 90,
            'vertex': 'O',
            'ray1': 'X',
            'ray2': 'Y',
            'color1': 'green',
            'color2': 'purple'
        },
        {
            'angle': 150,
            'vertex': 'P',
            'ray1': 'Q',
            'ray2': 'R',
            'color1': 'cyan',
            'color2': 'magenta'
        }
    ]

    files = draw_multiple_angles(angles, output_prefix='demo')

    print("\n=== Hoàn tất ===")
    print(f"Đã tạo {len(files) + 3} file ảnh")
    print("\nCách sử dụng đơn giản nhất:")
    print("  draw_angle(50)  # Vẽ góc AOB = 50°")
    print("  draw_angle(120, 'X', 'Y', 'Z')  # Vẽ góc XYZ = 120°")
    print("  draw_angle(75, 'O', 'M', 'N', 'purple', 'orange')  # Với màu tùy chỉnh")