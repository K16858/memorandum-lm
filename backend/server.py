from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uuid

# 仮システムメッセージ
sys_msg = """
あなたは「橘はづき」というメイド兼アシスタントです。以下のルールを厳密に守ってください。
1. 常に元気でくだけた口調で話す．
2. 会話の流れに沿った適切な応答を行う．
3. 一人称は「はづき」．
4. 同じようなことを繰り返してはいけない．
5. あなたはご主人様と会話しています．
6. 講義やメモに関する質問には親切に答えてください．
7. 要約や分析を求められたら丁寧に対応してください．
"""

app = FastAPI(title="MaidMemorandum API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Viteのデフォルトポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル
class Message(BaseModel):
    id: str
    content: str
    type: str  # "user", "ai", "summary", "keypoints"
    timestamp: datetime
    session_id: str

class Session(BaseModel):
    id: str
    title: str
    messages: List[Message]
    chat_messages: List[Dict[str, str]]
    created_at: datetime
    tags: List[str]

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class SummarizeRequest(BaseModel):
    text: str
    session_id: Optional[str] = None

class KeypointsRequest(BaseModel):
    text: str
    session_id: Optional[str] = None

# インメモリデータベース（DB化予定）
sessions: Dict[str, Session] = {}
active_connections: Dict[str, WebSocket] = {}

# セッション作成
def create_session(title: str = "New Session", system_prompt: str = sys_msg) -> Session:
    session_id = str(uuid.uuid4())
    session = Session(
        id=session_id,
        title=title,
        messages=[],
        chat_messages=[{"role": "system", "content": system_prompt}],  # システムメッセージで初期化
        created_at=datetime.now(),
        tags=[]
    )
    sessions[session_id] = session
    return session
