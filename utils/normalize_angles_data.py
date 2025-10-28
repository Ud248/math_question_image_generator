def normalize_angles_data(data):
    """
    Chuẩn hóa dữ liệu từ LLM thành list of dict
    
    Args:
        data: Có thể là dict (1 góc) hoặc list of dict (nhiều góc)
        
    Returns:
        list: Luôn trả về list of dict
    """
    # Nếu là dict đơn lẻ -> chuyển thành list có 1 phần tử
    if isinstance(data, dict):
        print("📦 Normalized: Single dict → List with 1 element")
        return [data]
    
    # Nếu đã là list -> giữ nguyên
    elif isinstance(data, list):
        print(f"📦 Normalized: Already a list with {len(data)} element(s)")
        return data
    
    # Trường hợp khác -> trả về list rỗng
    else:
        print("⚠️ Warning: Invalid data type, returning empty list")
        return []