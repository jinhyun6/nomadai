<template>
  <div class="login-container">
    <h1>디지털 노마드 AI - 로그인</h1>
    
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>이메일:</label>
        <input 
          type="email" 
          v-model="email" 
          placeholder="이메일을 입력하세요"
          required
        >
      </div>
      
      <div class="form-group">
        <label>비밀번호:</label>
        <input 
          type="password" 
          v-model="password" 
          placeholder="비밀번호를 입력하세요"
          required
        >
      </div>
      
      <button type="submit">로그인</button>
    </form>
    
    <p>
      계정이 없으신가요? 
      <a href="#" @click="$emit('switch-to-register')">회원가입</a>
    </p>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      fetch(`${process.env.VUE_APP_API_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.$emit('login-success', data.user);
        } else {
          alert(data.message);
        }
      })
      .catch(error => {
        console.error('로그인 오류:', error);
        alert('로그인 중 오류가 발생했습니다.');
      });
    }    
  }
}
</script>

<style scoped>
.login-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.login-container h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-weight: 600;
  font-size: 28px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 15px 20px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input::placeholder {
  color: #adb5bd;
}

.login-container button {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.login-container button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.login-container button:active {
  transform: translateY(0);
}

.login-container p {
  text-align: center;
  margin-top: 25px;
  color: #666;
  font-size: 14px;
}

.login-container a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-container a:hover {
  color: #764ba2;
  text-decoration: underline;
}
</style>