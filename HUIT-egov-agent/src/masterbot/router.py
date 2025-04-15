from openai import OpenAI
from src.common.config import Config

class MasterBot:
    def __init__(self, subbots, subbots_info):
        self.subbots = subbots
        self.subbots_info = subbots_info
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def classify_query(self, query):
        # Tạo danh sách danh mục với số thứ tự và mô tả
        subbots_description = "\n".join(
            f"{i+1}. {info['name']}: {info['description']}"
            for i, info in enumerate(self.subbots_info.values())
        )

        # System prompt – Định hướng hành vi
        system_prompt = (
            "Bạn là một trợ lý AI chuyên phân loại câu hỏi tiếng Việt. "
            "Nhiệm vụ của bạn là xác định danh mục phù hợp nhất cho một câu hỏi đầu vào, "
            "dựa trên mô tả các danh mục được cung cấp."
        )

        # User prompt – Nội dung yêu cầu
        user_prompt = f"""
        Dưới đây là danh sách các danh mục:

        {subbots_description}

        Câu hỏi: "{query}"

        → Hãy trả về **chỉ** tên danh mục phù hợp nhất (khớp đúng chính tả với danh sách trên),
        hoặc trả về `unknown` nếu không xác định được.
        """.strip()

        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        category = response.choices[0].message.content.strip()
        return category, subbots_description

    def process_query(self, query):
        category, masterbot_prompt = self.classify_query(query)
        # print(f"Debug - Category from LLM: '{category}'")
        # print(f"Debug - Available subbots: {list(self.subbots.keys())}")
        
        if category in self.subbots:
            response, subbot_prompts = self.subbots[category].process_query(query)
            return response, category, masterbot_prompt, subbot_prompts
        else:
            available_categories = ", ".join(self.subbots.keys())
            response = (f"Vui lòng cung cấp câu hỏi cụ thể hơn để tôi có thể hỗ trợ tốt nhất! "
                       f"Các chủ đề sẵn sàng hỗ trợ: {available_categories}.")
            return response, "unknown", masterbot_prompt, {}