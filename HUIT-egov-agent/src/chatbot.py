from openai import OpenAI
from src.common.config import Config
from src.common.vector_store import VectorStore
from src.common.functions import FUNCTIONS, execute_function

class Chatbot:
    def __init__(self, vector_store: VectorStore):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.vector_store = vector_store
        self.system_prompt = """
        Bạn là một trợ lý AI hỗ trợ người dùng sử dụng hệ thống HUIT eGov. 
        Dựa trên tài liệu hướng dẫn và dữ liệu cá nhân (nếu cần), hãy trả lời câu hỏi của người dùng một cách chính xác, ngắn gọn và hữu ích.
        """

    def get_embedding(self, text):
        response = self.client.embeddings.create(
            model=Config.EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding

    def handle_query(self, user_prompt):
        query_embedding = self.get_embedding(user_prompt)
        relevant_docs = self.vector_store.query(query_embedding, n_results=3)
        context = "\n".join(relevant_docs)
        # Rút gọn context để log
        short_context = (context[:100] + "...") if len(context) > 100 else context

        # Tạo user prompt đầy đủ để gửi API
        full_user_prompt = f"{user_prompt}\n\nHướng dẫn liên quan:\n{context}"
        # User prompt để log (gọn hơn)
        log_user_prompt = f"{user_prompt} (Context: {short_context})"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": full_user_prompt}
        ]
        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=messages,
            tools=FUNCTIONS,
            tool_choice="auto"
        )

        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            tool_info = []
            for tool_call in tool_calls:
                function_result = execute_function({
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                })
                tool_info.append({
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                })
                messages.append({
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                    ]
                })
                messages.append({
                    "role": "tool",
                    "name": tool_call.function.name,
                    "tool_call_id": tool_call.id,
                    "content": str(function_result)
                })
            final_response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=messages
            )
            return final_response.choices[0].message.content, {
                "system_prompt": self.system_prompt[:50] + "..." if len(self.system_prompt) > 50 else self.system_prompt,
                "user_prompt": log_user_prompt,
                "tool_calls": tool_info
            }

        return response.choices[0].message.content, {
            "system_prompt": self.system_prompt[:50] + "..." if len(self.system_prompt) > 50 else self.system_prompt,
            "user_prompt": log_user_prompt
        }