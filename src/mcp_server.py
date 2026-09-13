"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPFacilitiesServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "vinuni-facilities-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"

    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC
        """
        result_json = dispatch_tool_call(tool_name, arguments)
        content = json.loads(result_json)
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (vinuni-facilities-mcp-server)")
    print("==========================================================")

    server = MCPFacilitiesServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")

    # Kiểm tra trạng thái Tool Schema
    booking_tool = next((t for t in tools if t.get("name") == "create_booking"), None)
    if booking_tool and not booking_tool.get("parameters", {}).get("properties"):
        print("⏳ Tool 'create_booking' chưa được định nghĩa properties trong 'src/tools.py'.")
    else:
        print("✅ Tool 'create_booking' đã có schema đầy đủ.")

    # Kiểm tra hàm call_tool
    test_result = server.call_tool("check_room_availability", {"room_id": "P301", "datetime_str": "09:00 15/09/2026"})
    if not test_result:
        print("⏳ Hàm call_tool() đang trả về rỗng.")
    else:
        print(f"✅ Test dispatch tool 'check_room_availability' thành công:")
        print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")
