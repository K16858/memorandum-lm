from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uuid

# 仮システムプロンプト
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

MAX_MESSAGE = 20  # メッセージ履歴の最大数

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

# セッション取得
def get_session(session_id: str) -> Session:
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

# メッセージ追加
def add_message(session_id: str, content: str, message_type: str) -> Message:
    session = get_session(session_id)
    message = Message(
        id=str(uuid.uuid4()),
        content=content,
        type=message_type,
        timestamp=datetime.now(),
        session_id=session_id
    )
    session.messages.append(message)
    return message

# チャットメッセージ管理
def add_chat_message(session_id: str, role: str, content: str):
    session = get_session(session_id)
    session.chat_messages.append({"role": role, "content": content})
    
    # メッセージ履歴を制限（システムメッセージ + 最新n件）
    max_messages = MAX_MESSAGE
    if len(session.chat_messages) > max_messages:
        # システムメッセージは保持し，古いメッセージを削除
        session.chat_messages = [session.chat_messages[0]] + session.chat_messages[-(max_messages-1):]

# エンドポイント定義
@app.get("/")
async def root():
    return {"message": "MaidMemorandum API is running!"}

@app.get("/sessions")
async def get_sessions():
    return {"sessions": list(sessions.values())}

@app.post("/sessions")
async def create_new_session(title: str = "New Session"):
    session = create_session(title)
    return {"session": session}

@app.get("/sessions/{session_id}")
async def get_session_by_id(session_id: str):
    session = get_session(session_id)
    return {"session": session}
