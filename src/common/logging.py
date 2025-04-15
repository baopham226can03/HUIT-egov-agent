import json
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="logs/chatbot_log.jsonl"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(self, query, masterbot_result, selected_subbot, subbot_response, prompts=None):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "masterbot_result": masterbot_result,
            "selected_subbot": selected_subbot,
            "subbot_response": subbot_response,
        }


        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
