def new_feature(input_data):
    """增强版新功能
    Args:
        input_data: 数字类型输入
    Returns:
        处理后的结果或None
    """
    if not isinstance(input_data, (int, float)):
        print("错误：输入必须是数字")
        return None
    try:
        processed = input_data * 2
        print(f"处理结果: {processed}")
        return processed
    except Exception as e:
        print(f"处理错误: {str(e)}")
        return None