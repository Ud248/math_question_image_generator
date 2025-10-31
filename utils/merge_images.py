import os
from PIL import Image

def merge_images(image_files, output_filename="merged.png", direction="horizontal", gap=10):
    """
    Ghép nhiều ảnh lại thành một ảnh duy nhất
    
    Parameters:
    -----------
    image_files : list - Danh sách tên file ảnh cần ghép
    output_filename : str - Tên file output
    direction : str - "horizontal" (ngang) hoặc "vertical" (dọc)
    gap : int - Khoảng cách giữa các ảnh (pixel)
    """
    
    # Mở tất cả ảnh
    images = []
    for img_file in image_files:
        if os.path.exists(img_file):
            images.append(Image.open(img_file))
        else:
            print(f"⚠️ Không tìm thấy file: {img_file}")
            return
    
    if not images:
        print("❌ Không có ảnh nào để ghép!")
        return
    
    # Ghép ngang
    if direction == "horizontal":
        total_width = sum(img.width for img in images) + gap * (len(images) - 1)
        max_height = max(img.height for img in images)
        
        merged = Image.new('RGB', (total_width, max_height), 'white')
        
        x_offset = 0
        for img in images:
            merged.paste(img, (x_offset, 0))
            x_offset += img.width + gap
    
    # Ghép dọc
    else:  # vertical
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images) + gap * (len(images) - 1)
        
        merged = Image.new('RGB', (max_width, total_height), 'white')
        
        y_offset = 0
        for img in images:
            merged.paste(img, (0, y_offset))
            y_offset += img.height + gap
    
    # Lưu ảnh ghép
    merged.save(output_filename, dpi=(300, 300))
    merged.show()
    