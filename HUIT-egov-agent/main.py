from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml
from src.subbots.subbot import SubBot
from src.masterbot.router import MasterBot
from src.common.logging import Logger
from src.common.config import Config

app = FastAPI()
logger = Logger(log_file="logs/chatbot_log.jsonl") if Config.ENABLE_LOGGING else None

try:
    with open("bots_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise Exception("File bots_config.yaml not found. Please ensure it exists in the project root.")

subbots = {
    bot["name"]: SubBot(bot["name"], bot["data_path"], bot["collection_name"])
    for bot in config.get("bots", [])
}

subbots_info = {
    bot["name"]: {
        "name": bot["name"],
        "data_path": bot["data_path"],
        "collection_name": bot["collection_name"],
        "description": bot.get("description", "Không có mô tả")
    }
    for bot in config.get("bots", [])
}

masterbot = MasterBot(subbots, subbots_info)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    masterbot_result: str
    selected_subbot: str
    subbot_response: str


@app.post("/ask", response_model=QueryResponse)
async def ask_question(req: QueryRequest):
    try:
        # Xử lý truy vấn từ MasterBot
        response, category, masterbot_prompt, subbot_prompts = masterbot.process_query(req.query)

        log_info = {
            "query": req.query,
            "masterbot_result": category,
            "selected_subbot": category if category in subbots else "none",
            "subbot_response": response,
            "prompts": {
                "masterbot": masterbot_prompt,
                "subbot": subbot_prompts
            }
        }

        # Ghi log nếu cần
        if logger and Config.ENABLE_LOGGING:
            logger.log(**log_info)

        return QueryResponse(
            query=req.query,
            masterbot_result=log_info["masterbot_result"],
            selected_subbot=log_info["selected_subbot"],
            subbot_response=log_info["subbot_response"],
            prompts=log_info["prompts"]
        )

    except Exception as e:
        if logger and Config.ENABLE_LOGGING:
            logger.log(
                query=req.query,
                masterbot_result="error",
                selected_subbot="none",
                subbot_response=str(e)
            )
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
