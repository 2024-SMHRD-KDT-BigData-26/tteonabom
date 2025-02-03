<script>
    import { link } from 'svelte-spa-router';
  
    let userId = '';
    let password = '';
    let errorMessage = '';
  
    // ✅ 로그인 요청 함수
    async function handleLogin() {
        try {
            console.log("🔍 로그인 요청:", { userId, password });
  
            const payload = {
                USER_ID: userId,
                USER_PW: password
            };
  
            const response = await fetch("http://localhost:9000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
  
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "로그인 실패");
            }
  
            const result = await response.json();
            console.log("✅ 로그인 성공:", result);
  
            // ✅ JWT 토큰 저장 (로컬 스토리지)
            localStorage.setItem("access_token", result.access_token);
  
            // ✅ 로그인 성공 후 메인 페이지로 이동
            link("/home");
  
        } catch (error) {
            console.error("❌ 로그인 오류:", error.message);
            errorMessage = error.message;
        }
    }
  </script>

<style>
    /* 로고 이미지 반응형 스타일 */
  .img-fluid {
      margin-top: 70px; 
      max-width: 50%; 
      height: auto; 
      object-fit: contain; 
      margin: auto; /* 가운데 정렬 */
      display: block; /* 블록 요소로 설정 */
  }
  /* 로그인 제목 */
  .login_text {
      font-family: 'Paperlogy-6SemiBold';
      font-size: 28px;
      margin-top: 20px;
      margin-bottom: 20px;
  }
  /* 로그인 폼 컨테이너 */
  .form-container {
      text-align: center; /* 내부 텍스트 가운데 정렬 */
      margin: 0 auto; /* 가로 중앙 정렬 */
      margin-top: 50px; 
      justify-content: center; /* 가로 중앙 정렬 */
      align-items: center; /* 세로 중앙 정렬 */
      width: 500px; 
      height: 480px; 
      padding: 30px; 
      border: 1px solid #D9D9D9; 
      border-radius: 10px; 
      background-color: #fff; 
  }

  /* 입력 필드 */
  .form-control {
      height: 50px;
      width: 69%;
      font-size: 12px;
      padding: 10px;
      margin-top: 20px;
      margin-bottom: 20px;
      margin: auto;
      height: 44px; 
  }

  /* 로그인 버튼 */
  .login_btn {
      background-color: black; 
      color: #fff;
      border: none;
      width: 69%;
      height: 44px;  
      font-size: 14px;
      margin-top: 10px;
      border-radius: 5px;
  }
  .login_btn:hover {
      background-color: #333;
  }


  /* 구분선 */
  .separator {
      text-align: center;
      color: #6c757d;
      font-size: 14px;
      margin-top: 20px;
      margin-bottom: 20px;
      position: relative;
  }

  .separator::before,
  .separator::after {
      content: "";
      position: absolute;
      top: 50%;
      width: 100px;
      height: 1px;
      background: #ddd;
      transform: translateY(-50%); /* 세로 정렬 */
  }

  .separator::before {
      left: 70px;
  }

  .separator::after {
      right: 70px;
  }



  /* 회원가입 링크 */
  .register-link {
      color: #5a6268;
      font-size: 14px;
      text-decoration: none;
  }
</style>

<!-- 로그인 컨텐츠 영역 -->
<main class="content">
  <div class="container">
    <form class="form-container">
        <!-- 로그인 제목 -->
        <h3 class="login_text">로그인</h3>

        <!-- 아이디 입력 -->
        <div class="mb-3">
            <input type="text" id="userId" class="form-control" placeholder="아이디를 입력하세요" required>
        </div>

        <!-- 비밀번호 입력 -->
        <div class="mb-3">
            <input type="password" id="password" class="form-control" placeholder="비밀번호를 입력하세요" required>
        </div>

        <!-- 로그인 버튼 -->
        <button type="button" class="login_btn">로그인</button>

        <!-- 또는 -->
        <div class="separator my-3">또는</div>

        <!-- 카카오 로그인 -->
        <a id="kakao-login-btn" href="#">
            <img src="../src/assets/img/kakao_login.png" alt="카카오 로그인 버튼">
        </a>

        <!-- 회원가입 링크 -->
        <div class="text-center mt-3">
            <a use:link href="/Join" class="register-link">회원가입</a>
        </div>
    </form>
</div>
  </main>