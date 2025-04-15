import json

# Danh sách các hàm có thể gọi
FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_user_schedule",
            "description": "Lấy lịch cá nhân của người dùng từ hệ thống HUIT eGov.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "ID của người dùng"}
                },
                "required": ["user_id"]
            }
        }
    }
]

# Hàm giả lập truy xuất dữ liệu (thay bằng API thực tế nếu có)
def get_user_schedule(user_id):
    # Giả lập dữ liệu lịch
    return {
        "user_id": user_id,
        "schedule": [
            {"time": "09:00", "task": "Họp nhóm"},
            {"time": "14:00", "task": "Gửi báo cáo"}
        ]
    }

# Thực thi hàm dựa trên tên
def execute_function(function_call):
    function_name = function_call["name"]
    arguments = json.loads(function_call["arguments"])

    if function_name == "get_user_schedule":
        return get_user_schedule(arguments["user_id"])
    else:
        return {"error": f"Function {function_name} not implemented"}