from fastapi import FastAPI
import bcrypt
import os
import anthropic
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables, ChatMessage, engine, User
from sqlmodel import Session, select

app = FastAPI()

claude_client = anthropic.Anthropic(
    api_key=os.environ.get("CLAUDE_API_KEY")
)

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

class ChatRequest(BaseModel):
    message: str
    user_id: int
    user_name: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def say_hello():
    return {"message": "안녕하세요! 저는 노마드 AI입니다."}

@app.post("/chat")
def chat_with_ai(user_message: ChatRequest):
    
    with Session(engine) as session:
        user_msg = ChatMessage(
            user_id=user_message.user_id,
            sender=user_message.user_name,
            content=user_message.message)
        session.add(user_msg)
        session.commit()

    try:
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            system="""당신은 디지털 노마드 여행 전문가입니다. 다음 분야의 전문 지식을 가지고 있습니다:

여행 정보:
- 비자 요구사항 및 신청 절차
- 항공료 최저가 찾는 방법
- 숙소 추천 (에어비앤비, 호텔, 게스트하우스)
- 현지 교통수단 및 이동 팁

디지털 노마드 전용:
- 인터넷 속도 및 카페/코워킹 스페이스 정보
- 시차 관리 및 업무 효율성
- 노마드 비자 및 장기 체류 방법
- 세금 및 법적 고려사항

예산 관리:
- 국가별 생활비 정보
- 현지 물가 및 환율 팁
- 여행자 보험 추천

항상 친근하고 실용적인 조언을 제공하며, 구체적인 웹사이트나 앱을 추천할 때는 정확한 정보를 제공하세요.""",
            messages=[
                {"role": "user", "content": user_message.message}
            ]
        )
        ai_response = response.content[0].text
    except Exception as e:
        ai_response = f"ai 답변 못받음 try에서: {str(e)}"
    
    with Session(engine) as session:
        ai_msg = ChatMessage(
            sender="AI", 
            content=ai_response, 
            user_id=user_message.user_id
        )
        session.add(ai_msg)
        session.commit()

    return {"response": ai_response}

@app.post("/register")
def register_user(user_data: UserRegister):
    try:
        with Session(engine) as session:
            existing_user = session.exec(select(User).where(User.email == user_data.email)).first()

            if existing_user:
                return {"success":False, "message": "이미 존재하는 계정입니다."}
            
            hashed_password = hash_password(user_data.password)
            new_user = User(
                name=user_data.name,
                email=user_data.email,
                password=hashed_password
            )
            session.add(new_user)
            session.commit()
            return {"success": True, "message": "회원가입이 완료되었습니다."}

    except Exception as e:
        return {"success": False, "message": f"회원가입 중 오류가 발생했습니다: {str(e)}"}

@app.post("/login")
def login_user(user_data: UserLogin):
    try:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == user_data.email)).first()

            if not user:
                return {"success": False, "message": "존재하지 않는 이메일입니다."}

            if verify_password(user_data.password, user.password):
                return {
                    "success": True,
                    "message": "로그인 성공!",
                    "user":{
                        "id": user.id,
                        "name": user.name,
                        "email": user.email
                    }
                } 
            else:
                return {"success": False, "message": "비밀번호가 틀렸습니다."}
    
    except Exception as e:
        return {"success": False, "message": f"로그인 중 오류가 발생했습니다: {str(e)}"}

@app.get("/messages/{user_id}")
def get_user_messages(user_id: int):
    try:
        with Session(engine) as session:
            messages = session.exec(
                select(ChatMessage).where(
                    ChatMessage.user_id == user_id
                ).order_by(ChatMessage.timestamp)
            ).all()

            return {"messages": messages}

    except Exception as e:
        return {"success": False, "message": f"메시지 조회 중 오류가 발생했습니다: {str(e)}"}   