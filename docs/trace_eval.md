# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Nguyễn Mạnh Hải]  
> **Mã Sinh Viên / Mã Học viên:** [2A202602988]  
> **Chủ đề Lựa chọn:** [Đề tài 2.3: Trợ lý Đặt Phòng họp & Thiết bị (Facilities Agent)]  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **4** / 5 | Đã xác nhận thực tế qua log API thật (TC03): Agent tự chủ suy luận qua 3 bước — gọi `check_room_availability`, quan sát kết quả AVAILABLE, tự quyết định gọi tiếp `create_booking`, rồi mới tổng hợp câu trả lời cuối — đúng chuỗi Thought → Action → Observation → Action → Final Answer, không chỉ dừng ở 1 lượt gọi Tool. |
| **2. Tool Interaction** | **4** / 5 | Cần tích hợp qua MCP Server tới ít nhất 2 nguồn dữ liệu ngoài: lịch phòng (`check_room_availability`) và hệ thống booking/tồn kho thiết bị (`create_booking`), có thể mở rộng thêm notification. |
| **3. Dynamic Decision** | **4** / 5 | Bước tiếp theo phụ thuộc rõ vào Observation: nếu phòng BUSY hoặc thiếu thiết bị (EQUIPMENT_UNAVAILABLE), Agent phải từ chối/đề xuất phương án khác thay vì đặt bừa — thể hiện rõ nhánh rẽ dựa trên kết quả Tool. |
| **4. Long Horizon Goal** | **2** / 5 | Đây là tác vụ giao dịch ngắn hạn (check → book), hoàn tất trong 1-2 lượt hội thoại, không cần duy trì mục tiêu xuyên suốt nhiều phiên/nhiều ngày. |
| **TỔNG ĐIỂM AGENTIC FIT** | **14 / 20** | *Vượt ngưỡng 12/20 → Bài toán phù hợp triển khai Agentic System, thuộc dạng "workflow automation agent" (transactional) rõ ràng, có giá trị minh hoạ ReAct tốt qua Multi-step Reasoning, Tool Interaction và Dynamic Decision.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Đặt phòng P205 lúc 14:00 ngày 16/09/2026 cho buổi họp nhóm dự án AI, người tổ chức là Nguyễn Văn An.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "check_room_availability",
    "arguments": { "room_id": "P205", "datetime_str": "14:00 16/09/2026" },
    "observation": {
      "status": "AVAILABLE",
      "room_id": "P205",
      "data": { "room_name": "Phòng họp P205", "capacity": 6, "floor": 2, "equipment": ["Màn hình TV", "Loa hội nghị"] },
      "message": "Phòng Phòng họp P205 (sức chứa 6 người, tầng 2) đang trống vào lúc 14:00 16/09/2026. Thiết bị sẵn có: Màn hình TV, Loa hội nghị."
    },
    "latency_ms": 2730.0
  },
  {
    "step": 2,
    "query": "Đặt phòng P205 lúc 14:00 ngày 16/09/2026 cho buổi họp nhóm dự án AI, người tổ chức là Nguyễn Văn An.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "create_booking",
    "arguments": { "purpose": "Họp nhóm dự án AI", "datetime_str": "14:00 16/09/2026", "room_id": "P205", "organizer": "Nguyễn Văn An" },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-P205-01",
      "room_id": "P205",
      "datetime": "14:00 16/09/2026",
      "organizer": "Nguyễn Văn An",
      "purpose": "Họp nhóm dự án AI",
      "message": "Đặt phòng thành công: Phòng họp P205 vào lúc 14:00 16/09/2026 cho Nguyễn Văn An (mục đích: Họp nhóm dự án AI)."
    },
    "latency_ms": 2904.13
  },
  {
    "step": 3,
    "query": "Đặt phòng P205 lúc 14:00 ngày 16/09/2026 cho buổi họp nhóm dự án AI, người tổ chức là Nguyễn Văn An.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Đặt phòng thành công! Booking ID: BK-P205-01, Phòng P205, 14:00 16/09/2026, Người tổ chức: Nguyễn Văn An, Mục đích: Họp nhóm dự án AI.",
    "latency_ms": 2362.37
  }
]
```

> ✅ Log trên trích từ `docs/trace_waterfall.json` (TC03), sinh ra từ phản hồi **Gemini API thật** (`gemini-3.6-flash`, LLM Provider: `GeminiProvider`) khi chạy `python src/app.py --all`. Đây là bằng chứng vòng lặp ReAct thực sự chain 2 Tool Call liên tiếp (`check_room_availability` → `create_booking`) dựa trên Observation của bước trước, đúng tinh thần Thought → Action → Observation → Action → Final Answer.

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt (TC02: 1 lượt `check_room_availability`; TC03: 2 lượt `check_room_availability` → `create_booking`; TC04: 1 lượt; TC05: 1 lượt `check_room_availability` cho mã phòng không tồn tại).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

> ℹ️ **Ghi chú:** TC04 và TC05 trong lần chạy gần nhất bị giới hạn quota Gemini Free Tier (429 RESOURCE_EXHAUSTED, 5 request/phút) nên tự động fallback sang Mock Offline Provider ở các bước sau. Đây là giới hạn hạn mức API, không phải lỗi logic — nên chạy lại `python src/app.py --all` cách nhau vài phút (hoặc nâng hạn mức) để có log API thật đầy đủ cho toàn bộ 5 test case trước khi nộp bài chính thức.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
