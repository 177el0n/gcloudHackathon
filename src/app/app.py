from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import Message
from agent.agent_create import AgentCreate

app = FastAPI()

# CORSミドルウェアの設定（異なるオリジン間でのやり取りに必要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # リクエストを許可するドメイン名（今は全てのオリジンを許可）
    allow_credentials=False,  # 認証情報（cookieなど）を許可するかどうか
    allow_methods=["*"],  # 許可するHTTPメソッドを指定
    allow_headers=["*"],  # 許可するHTTPヘッダーの指定
)

@app.post("/bot")
async def root(user_message: Message):
    print(f"受信したメッセージ： {user_message.message}")
    user_text = user_message.message

    bot_reply = f"あなたは「'{user_text}'」と言いました。"
    print(f"Botの返信： {bot_reply}")

    agent = AgentCreate(user_text)
    response = agent.workflow()
    return {"reply": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
