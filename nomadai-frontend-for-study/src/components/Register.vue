<template>
  <div class="register-container">
    <h1>디지털 노마드 AI - 회원가입</h1>
    
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>이름:</label>
        <input 
          type="text" 
          v-model="name" 
          placeholder="이름을 입력하세요"
          required
        >
      </div>
      
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
      
      <div class="form-group">
        <label>비밀번호 확인:</label>
        <input 
          type="password" 
          v-model="confirmPassword" 
          placeholder="비밀번호를 다시 입력하세요"
          required
        >
      </div>
      
      <button type="submit">회원가입</button>
    </form>
    
    <p>
      이미 계정이 있으신가요? 
      <a href="#" @click="$emit('switch-to-login')">로그인</a>
    </p>
  </div>
</template>

<script>
export default {
  name: 'UserRegister',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
      }
      fetch(`${process.env.VUE_APP_API_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.name,
          email: this.email,
          password: this.password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('회원가입이 완료되었습니다!');
          this.$emit('switch-to-login');
        } else {
          alert(data.message);
        }
      })
      .catch(error => {
        console.error('회원가입 오류:', error);
        alert('회원가입 중 오류가 발생했습니다.');
      });
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.register-container h1 {
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
  border-color: #28a745;
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
}

.form-group input::placeholder {
  color: #adb5bd;
}

.register-container button {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.register-container button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
}

.register-container button:active {
  transform: translateY(0);
}

.register-container p {
  text-align: center;
  margin-top: 25px;
  color: #666;
  font-size: 14px;
}

.register-container a {
  color: #28a745;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.register-container a:hover {
  color: #20c997;
  text-decoration: underline;
}
</style>