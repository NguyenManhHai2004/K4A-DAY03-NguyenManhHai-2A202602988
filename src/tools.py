"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Kiểm tra tình trạng trống của phòng họp và thiết bị sẵn có
    {
        "name": "check_room_availability",
        "description": "Kiểm tra tình trạng trống của phòng họp và danh sách thiết bị sẵn có tại một thời điểm cụ thể.",
        "parameters": {
            "type": "object",
            "properties": {
                "room_id": {
                    "type": "string",
                    "description": "Mã phòng họp cần kiểm tra (ví dụ: 'P301')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian cần kiểm tra (ví dụ: '09:00 15/09/2026')"
                }
            },
            "required": ["room_id", "datetime_str"]
        }
    },

    # Tool 2: Tạo booking đặt phòng họp kèm thiết bị yêu cầu
    {
        "name": "create_booking",
        "description": "Tạo booking đặt phòng họp kèm thiết bị yêu cầu cho người tổ chức.",
        "parameters": {
            "type": "object",
            "properties": {
                "room_id": {
                    "type": "string",
                    "description": "Mã phòng họp cần đặt (ví dụ: 'P301')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian đặt phòng (ví dụ: '09:00 15/09/2026')"
                },
                "organizer": {
                    "type": "string",
                    "description": "Tên người tổ chức cuộc họp"
                },
                "purpose": {
                    "type": "string",
                    "description": "Mục đích cuộc họp (ví dụ: 'Họp nhóm dự án')"
                },
                "equipment_needed": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách thiết bị cần dùng (ví dụ: ['Máy chiếu'])"
                }
            },
            "required": ["room_id", "datetime_str", "organizer"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_ROOMS = {
    "P301": {
        "room_name": "Phòng họp P301",
        "capacity": 10,
        "floor": 3,
        "equipment": ["Máy chiếu", "Màn hình TV", "Bảng trắng"],
        "booked_slots": []
    },
    "P205": {
        "room_name": "Phòng họp P205",
        "capacity": 6,
        "floor": 2,
        "equipment": ["Màn hình TV", "Loa hội nghị"],
        "booked_slots": []
    }
}


def execute_check_room_availability(room_id: str, datetime_str: str) -> str:
    """Thực thi kiểm tra tình trạng trống của phòng họp theo mã phòng và thời gian"""
    room = MOCK_ROOMS.get(room_id.strip().upper())
    if not room:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phòng họp có mã '{room_id}'."
        }, ensure_ascii=False)
    if datetime_str in room["booked_slots"]:
        return json.dumps({
            "status": "BUSY",
            "room_id": room_id,
            "message": f"Phòng {room['room_name']} đã có lịch vào lúc {datetime_str}, vui lòng chọn khung giờ khác."
        }, ensure_ascii=False)
    return json.dumps({
        "status": "AVAILABLE",
        "room_id": room_id,
        "data": {
            "room_name": room["room_name"],
            "capacity": room["capacity"],
            "floor": room["floor"],
            "equipment": room["equipment"]
        },
        "message": (
            f"Phòng {room['room_name']} (sức chứa {room['capacity']} người, tầng {room['floor']}) "
            f"đang trống vào lúc {datetime_str}. Thiết bị sẵn có: {', '.join(room['equipment'])}."
        )
    }, ensure_ascii=False)


def execute_create_booking(room_id: str, datetime_str: str, organizer: str, purpose: str = "Họp nhóm", equipment_needed: list = None) -> str:
    """Thực thi tạo booking đặt phòng họp kèm thiết bị yêu cầu"""
    room = MOCK_ROOMS.get(room_id.strip().upper())
    if not room:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phòng họp có mã '{room_id}'."
        }, ensure_ascii=False)
    if datetime_str in room["booked_slots"]:
        return json.dumps({
            "status": "CONFLICT",
            "message": f"Phòng {room['room_name']} đã được đặt vào lúc {datetime_str}, không thể đặt trùng lịch."
        }, ensure_ascii=False)
    missing_equipment = [e for e in (equipment_needed or []) if e not in room["equipment"]]
    if missing_equipment:
        return json.dumps({
            "status": "EQUIPMENT_UNAVAILABLE",
            "message": f"Phòng {room['room_name']} không có thiết bị: {', '.join(missing_equipment)}. Vui lòng chọn phòng khác hoặc bỏ bớt yêu cầu thiết bị."
        }, ensure_ascii=False)
    room["booked_slots"].append(datetime_str)
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{room_id}-{len(room['booked_slots']):02d}",
        "room_id": room_id,
        "datetime": datetime_str,
        "organizer": organizer,
        "purpose": purpose,
        "message": f"Đặt phòng thành công: {room['room_name']} vào lúc {datetime_str} cho {organizer} (mục đích: {purpose})."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "check_room_availability": execute_check_room_availability,
    "create_booking": execute_create_booking
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
