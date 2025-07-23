<template>
  <div id="app">
    <!-- 로그인하지 않은 경우 -->
    <div v-if="!isLoggedIn">
      <!-- 로그인 페이지 -->
      <UserLogin 
        v-if="currentView === 'login'" 
        @switch-to-register="currentView = 'register'"
        @login-success="handleLoginSuccess"
      />
      
      <!-- 회원가입 페이지 -->
      <UserRegister 
        v-if="currentView === 'register'" 
        @switch-to-login="currentView = 'login'"
        @register-success="handleRegisterSuccess"
      />
    </div>
    
    <!-- 로그인한 경우 - 기존 채팅 화면 -->
    <div v-if="isLoggedIn">
      <div class="header">
        <h1>디지털 노마드 AI 챗봇</h1>
        <div>
          <span v-if="currentUser">{{ currentUser.name }}님 반갑습니다!</span>
          <button @click="logout" class="logout-btn">로그아웃</button>
        </div>
      </div>
      
      <div class="chat-container">
        <div class="chat-messages">
          <p 
            v-for="message in messages" 
            :key="message.text"
            :class="message.sender === 'AI' ? 'ai-message' : 'user-message'"
          >
            {{ message.sender }}: {{ message.text }}
          </p>
        </div>
        
        <div class="chat-input">
          <input type="text" v-model="userMessage" placeholder="메시지를 입력하세요...">
          <button @click="sendMessage">전송</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserLogin from './components/Login.vue'  
import UserRegister from './components/Register.vue'

export default {
  name: 'App',
  components: {
    UserLogin,
    UserRegister
  },
  data() {
    return {
      isLoggedIn: false,
      currentView: 'login', 
      currentUser: null,
      userMessage: '',
      messages: []
    }
  },
  mounted() {
    // 로그인한 경우에만 채팅 기록 불러오기
    if (this.isLoggedIn) {
      this.loadChatHistory();
    }
  },
  methods: {
    handleLoginSuccess(user) {
      this.isLoggedIn = true;
      this.currentUser = user;
      this.loadChatHistory();
    },
    
    handleRegisterSuccess() {
      this.isLoggedIn = true;
      this.loadChatHistory();
    },
    
    logout() {
      this.isLoggedIn = false;
      this.currentView = 'login';
      this.currentUser = null;
      this.messages = [];
    },
    
    sendMessage() {
      if (this.userMessage.trim() !== '') {
        const currentMessage = this.userMessage;
        this.messages.push({ sender: this.currentUser.name, text: currentMessage });
        this.userMessage = '';
        
        fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: currentMessage,
            user_id: this.currentUser.id,
            user_name: this.currentUser.name })
        })
        .then(response => response.json())
        .then(data => {
          this.messages.push({ sender: 'AI', text: data.response });
        });
      }
    },
    
    loadChatHistory() {
      fetch(`/api/messages/${this.currentUser.id}`)
        .then(response => response.json())
        .then(data => {
          this.messages = data.messages.map(msg => ({
            sender: msg.sender,
            text: msg.content
          }));
        })
        .catch(error => {
          console.error('채팅 기록을 불러오는데 실패했습니다:', error);
        });
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: white;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header div {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header span {
  color: white;
  font-weight: 500;
}

.logout-btn {
  padding: 8px 16px;
  background: rgba(220, 53, 69, 0.8);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 1);
  transform: translateY(-2px);
}

.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  height: 500px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
  background: white;
  scrollbar-width: thin;
  scrollbar-color: #e0e0e0 transparent;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #e0e0e0;
  border-radius: 3px;
}

.chat-messages p {
  margin: 15px 0;
  padding: 12px 18px;
  border-radius: 18px;
  max-width: 80%;
  line-height: 1.4;
  word-wrap: break-word;
}

.chat-messages p.user-message {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  margin-left: auto;
  text-align: right;
}

.chat-messages p.ai-message {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #e9ecef;
  margin-right: auto;
  text-align: left;
}

.chat-input {
  display: flex;
  padding: 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  gap: 12px;
}

.chat-input input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #e9ecef;
  border-radius: 25px;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
}

.chat-input input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-input button {
  padding: 15px 25px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 80px;
}

.chat-input button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.chat-input button:active {
  transform: translateY(0);
}
</style>
