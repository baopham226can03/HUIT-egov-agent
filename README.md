# HUIT eGov Chatbot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green) ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange) ![License](https://img.shields.io/badge/License-MIT-yellow)

**HUIT eGov Chatbot** là một trợ lý AI thông minh được thiết kế để hỗ trợ người dùng sử dụng hệ thống HUIT eGov. Dự án tích hợp Retrieval-Augmented Generation (RAG) với OpenAI API và ChromaDB để cung cấp câu trả lời chính xác dựa trên tài liệu hướng dẫn, đồng thời hỗ trợ truy xuất dữ liệu cá nhân thông qua function calling.

## Mục tiêu dự án

- **Hỗ trợ người dùng**: Cung cấp hướng dẫn chi tiết về cách sử dụng hệ thống HUIT eGov thông qua giao tiếp tự nhiên.
- **Tích hợp API**: Sử dụng OpenAI API kết hợp với ChromaDB để trả lời câu hỏi người dùng từ tài liệu hướng dẫn và dữ liệu cá nhân.
- **Dễ mở rộng**: Thiết kế mô-đun hóa để dễ dàng thêm tính năng hoặc tích hợp với các API thực tế của HUIT eGov.

## Tính năng chính

1. **Truy xuất thông tin từ tài liệu**:
   - Tự động xử lý và lưu trữ nội dung PDF hướng dẫn vào vector store.
   - Truy xuất nội dung liên quan dựa trên câu hỏi của người dùng.
2. **Function Calling**:
   - Hỗ trợ gọi các hàm để lấy dữ liệu cá nhân (hiện tại giả lập với `get_user_schedule`).
3. **Giao tiếp thông minh**:
   - Sử dụng mô hình `gpt-4o-mini` của OpenAI để tạo câu trả lời tự nhiên và chính xác.
4. **Xử lý văn bản lớn**:
   - Chia nhỏ nội dung PDF thành các chunk để tránh vượt giới hạn token của OpenAI API.
5. **Phân hệ động**: 
   - Sử dụng `masterbot` để phân loại câu hỏi và chuyển hướng đến `subbot` phù hợp dựa trên các phân hệ (ví dụ: tài chính, học vụ).

## Cấu trúc dự án
```
huit_egov_chatbot/
├── data/                    # Thư mục chứa dữ liệu PDF theo phân hệ
│   ├── Data1/            # PDF hướng dẫn về lĩnh vực 1
│   │   ├── guide1.pdf
│   │   └── ...
│   ├── Data2/            # PDF hướng dẫn về lĩnh vực 2
│   │   ├── guide2.pdf
│   │   └── ...
│   └── ...                 # Các phân hệ khác
├── src/                    # Thư mục chứa mã nguồn
│   ├── common/             # Code dùng chung
│   │   ├── init.py
│   │   ├── config.py       # Cấu hình
│   │   ├── vector_store.py # Quản lý ChromaDB
│   │   ├── pdf_processor.py # Xử lý PDF
│   │   └── functions.py    # Hàm function calling
│   ├── masterbot/          # Logic của masterbot
│   │   ├── init.py
│   │   └── router.py       # Phân loại và chuyển hướng
│   ├── subbots/            # Logic của subbot
│   │   ├── init.py
│   │   └── subbot.py       # Class SubBot tổng quát
│   ├── init.py
│   └── chatbot.py          # Logic chatbot chung
├── bots_config.yaml        # File cấu hình subbots
├── .env                    # File chứa biến môi trường (không commit lên git)
├── main.py                 # File chạy chính
├── requirements.txt        # Danh sách thư viện cần cài đặt
└── README.md               # Tài liệu hướng dẫn (bạn đang đọc)
```

### Chi tiết các file

- **`main.py`**: Điểm khởi đầu, khởi tạo `masterbot` và các `subbots` từ cấu hình, chạy vòng lặp chatbot.
- **`src/config.py`**: Load biến môi trường từ `.env` (API key, model).
- **`src/vector_store.py`**: Quản lý ChromaDB để lưu trữ và truy xuất embeddings theo collection riêng cho từng subbot.
- **`src/pdf_processor.py`**: Đọc PDF, chia nhỏ nội dung, tạo embeddings và lưu vào vector store.
- **`src/functions.py`**: Định nghĩa các hàm function calling (hiện có `get_user_schedule`).
- **`src/chatbot.py`**: Xử lý câu hỏi người dùng, tích hợp RAG và function calling cho từng subbot.
- **`src/masterbot/router.py`**: Phân loại câu hỏi và chuyển hướng đến subbot phù hợp.
- **`src/subbots/subbot.py`**: Class tổng quát để khởi tạo và xử lý từng phân hệ.
- **`bots_config.yaml`**: Cấu hình danh sách subbots (tên, đường dẫn dữ liệu, collection).

## Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Hệ điều hành**: Windows, macOS, Linux
- **Kết nối internet**: Để gọi OpenAI API
- **Dung lượng**: Tối thiểu 1GB RAM, 500MB ổ cứng (tùy thuộc vào số lượng PDF)

## Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/yourusername/huit_egov_chatbot.git
cd huit_egov_chatbot
```

### 2. Tạo file .env

Tạo file `.env` trong thư mục gốc với nội dung sau (thay bằng giá trị thực tế của bạn):

```ini
OPENAI_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4o-mini
INDEX_NAME=huit_egov
```

- `OPENAI_API_KEY`: Khóa API từ OpenAI (bắt buộc).
- `LLM_MODEL`: Mô hình LLM, mặc định là `gpt-4o-mini`.
- `INDEX_NAME`: Tên collection trong ChromaDB, phải từ 3-63 ký tự (ví dụ: `huit_egov`).

### 3. Cài đặt thư viện

Chạy lệnh sau để cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Các thư viện bao gồm:

- `openai`: Gọi API OpenAI.
- `chromadb`: Vector database.
- `PyPDF2`: Đọc file PDF.
- `python-dotenv`: Load biến môi trường.
- `tqdm`: Thanh tiến trình.
- `pyyaml`: Đọc file cấu hình YAML.


### 4. Chuẩn bị dữ liệu

- Tạo các thư mục con trong `data/` và đặt các file PDF hướng dẫn tương ứng..
- Đảm bảo ít nhất một file PDF tồn tại để chatbot có dữ liệu xử lý.

## Cách sử dụng

### Chạy chương trình

```bash
uvicorn main:app --reload --port 8000
```

### Cách dùng API
```bash
curl -X POST http://127.0.0.1:8000/ask \ -H "Content-Type: application/json" \ -d "{\"query\": \"Làm sao để có thể đăng nhập được ở app Bình Thuận"}"
```

Chương trình sẽ:

1. Khởi tạo các subbots từ bots_config.yaml, xử lý PDF trong từng thư mục và lưu vào ChromaDB.
2. Khởi tạo masterbot để phân loại và chuyển hướng câu hỏi.


## Quy trình hoạt động

1. **User Prompt**: Người dùng nhập câu hỏi (ví dụ: "Học phí kỳ này bao nhiêu?").
2. **MasterBot**:
 - Phân loại câu hỏi bằng LLM để xác định phân hệ phù hợp (ví dụ: FinanceBot).
 - Chuyển hướng câu hỏi đến subbot tương ứng.
3. **SubBot**:
 - Embedding câu hỏi bằng text-embedding-ada-002.
 - Truy xuất 3 đoạn nội dung liên quan nhất từ ChromaDB.
 - Gửi câu hỏi, system prompt, nội dung truy xuất và danh sách hàm đến gpt-4o-mini.
 - Nếu cần, gọi hàm (ví dụ: get_user_schedule) và gửi kết quả trở lại model.
 - Model tạo câu trả lời cuối cùng.
4. **Trả lời**: Chatbot hiển thị câu trả lời cho người dùng.

## Tùy chỉnh và mở rộng

### Thêm hàm mới

Mở `src/functions.py`, thêm định nghĩa hàm vào `FUNCTIONS`:

```python
{
    "type": "function",
    "function": {
        "name": "get_user_info",
        "description": "Lấy thông tin người dùng",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "ID của người dùng"}
            },
            "required": ["user_id"]
        }
    }
}
```

Thêm logic thực thi trong `execute_function`:

```python
if function_name == "get_user_info":
    return {"user_id": arguments["user_id"], "name": "Nguyen Van A"}
```

### Tích hợp API thực tế

Thay hàm giả lập trong `src/functions.py` bằng API khác:

```python
import requests

def get_user_schedule(user_id):
    response = requests.get(f"https://example-api")
    return response.json()
```

## Xử lý lỗi thường gặp

 - **ModuleNotFoundError**: Kiểm tra pip install -r requirements.txt đã chạy thành công.
 - **ValueError**: Expected collection name...: Đảm bảo collection_name trong bots_config.yaml từ 3-63 ký tự.
 - **openai.BadRequestError**: maximum context length: Đảm bảo pdf_processor.py chia nhỏ nội dung PDF đúng cách.
 - **openai.BadRequestError**: Missing tools[0].type: Kiểm tra FUNCTIONS trong src/common/functions.py có trường "type": "function".
 - **unknown phân hệ**: Kiểm tra debug output trong masterbot/router.py để đảm bảo tên danh mục từ LLM khớp với subbots.
