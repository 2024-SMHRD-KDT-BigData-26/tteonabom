<script>
    import '../assets/css/Login.css';
    import { onMount, tick } from 'svelte';
    import { link } from 'svelte-spa-router';

    let userId = "";
    let password = "";
    let errorMessage = "";
    let rememberId = false;  // 체크박스 상태를 바인딩할 변수

    // onMount에서 Kakao SDK 초기화
    onMount(() => {
        const savedUserId = localStorage.getItem("userId");
        if (savedUserId) {
            userId = savedUserId;
            rememberId = true; // 아이디 저장이 체크된 상태
        }

        if (window.Kakao) {
            window.Kakao.init("587fbaebd1683e7353f73fee72da4cdc");  // Kakao JavaScript 키
            console.log("Kakao 초기화 성공:", window.Kakao.isInitialized());
        } else {
            console.error("Kakao SDK 로드 실패");
        }
    });

    // 카카오 로그인 함수
    async function kakaoLogin() {
        if (!window.Kakao) {
            console.error("Kakao SDK가 초기화되지 않았습니다.");
            return;
        }

        // 필요한 동의 항목(scope)을 요청합니다.
        window.Kakao.Auth.login({
            scope: 'profile_nickname, profile_image, account_email',
            success: function(authObj) {
                console.log("Kakao 인증 성공:", authObj);

                window.Kakao.API.request({
                    url: '/v2/user/me',
                    success: function(response) {
                        console.log("Kakao 사용자 정보:", response);

                        // 프로필 정보가 두 가지 위치에 있을 수 있으므로, 둘 다 확인합니다.
                        const profile = (response.kakao_account && response.kakao_account.profile) || response.properties;
                        
                        if (!profile) {
                            console.error("사용자 프로필 정보가 제공되지 않았습니다. 추가 동의가 필요할 수 있습니다.");
                            errorMessage = "사용자 프로필 정보가 제공되지 않았습니다. 추가 동의 후 다시 시도해주세요.";
                            return;
                        }

                        // Kakao 고유 ID를 기반으로 사용자 아이디 생성 (예: "kakao_1234567890")
                        const kakaoUserId = `kakao_${response.id}`;
                        const userData = {
                            USER_ID: kakaoUserId,
                            USER_NICK: profile.nickname,
                            // 소셜 로그인 사용자는 별도의 비밀번호 없이 임의의 값을 사용합니다.
                            USER_PW: "KAKAO_SOCIAL_USER",
                            // 프로필 이미지의 필드명이 다를 수 있으므로 두 가지를 모두 확인합니다.
                            USER_PROFILE_IMG: profile.profile_image_url || profile.profile_image,
                        };

                        // 백엔드에 사용자 데이터를 전송하여 로그인/회원가입 처리
                        fetch("http://localhost:9000/api/kakao-login", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify(userData),
                        })
                        .then(res => res.json())
                        .then(data => {
                            console.log("백엔드 응답:", data);
                            localStorage.setItem("user", JSON.stringify(data));
                            window.dispatchEvent(new Event('storage'));
                            tick().then(() => {
                                window.location.href = "/";
                            });
                        })
                        .catch(err => {
                            console.error("백엔드 통신 오류:", err);
                            errorMessage = "카카오 로그인 처리 중 오류가 발생했습니다.";
                        });
                    },
                    fail: function(error) {
                        console.error("Kakao 사용자 정보 요청 실패:", error);
                        errorMessage = "Kakao 사용자 정보 요청에 실패했습니다.";
                    }
                });
            },
            fail: function(err) {
                console.error("Kakao 로그인 실패:", err);
                errorMessage = "카카오 로그인에 실패했습니다.";
            }
        });
    }

    // 로그인 함수 수정: 아이디 저장 상태에 따라 로컬스토리지에 아이디 저장
    async function login() {
        errorMessage = ""; // 오류 메시지 초기화

        if (!userId || !password) {
            errorMessage = "아이디와 비밀번호를 입력하세요.";
            return;
        }

        // 아이디 저장 여부 체크
        if (rememberId) {
            localStorage.setItem("userId", userId);  // 로컬스토리지에 아이디 저장
        } else {
            localStorage.removeItem("userId");  // 아이디 저장 안 할 경우 로컬스토리지에서 삭제
        }

        try {
            const payload = {
                USER_ID: userId,  // 백엔드에서 기대하는 필드명
                USER_PW: password,  // 백엔드에서 기대하는 필드명
            };

            const response = await fetch("http://localhost:9000/api/login", {
                method: "POST",
                mode: "cors", // CORS 설정
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),  // 올바른 필드명으로 요청
            });

            const data = await response.json();

            if (!response.ok) {
                errorMessage = data.detail?.error || "로그인에 실패했습니다.";
                return;
            }

            // 로그인 성공 시 localStorage에 사용자 정보 저장
            localStorage.setItem("user", JSON.stringify(data));

            // 로그인 상태 즉시 업데이트 (네비게이션 반영을 위해)
            window.dispatchEvent(new Event('storage'));

            // UI가 즉시 업데이트되도록 강제 갱신
            await tick();

            // 메인 페이지로 이동
            window.location.href = "/";

        } catch (error) {
            errorMessage = "서버 오류가 발생했습니다.";
            console.error("로그인 오류:", error);
        }
    }
</script>
  
  <style>
    .content{
        height: 729px;
        display: flex;
        justify-content: center; /* 가로 중앙 정렬 */
        align-items: center; /* 세로 중앙 정렬 */
    }
    .container {
        margin: 0 auto; /* 가로 중앙 정렬 */ 
    }
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
        justify-content: center; /* 가로 중앙 정렬 */
        align-items: center; /* 세로 중앙 정렬 */
        width: 500px; 
        min-height: 510px; 
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

    .rememberId-div {
        padding-right: 210px;
    }

    /* 체크박스 스타일 */
    input[type="checkbox"] {
        margin-right: 8px;
    }

    .rememberId {
        margin-top: -20px;
        font-size: 14px;
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
    
    .no-id {
        color: #FF5D17;
        font-size: 14px;
        text-decoration: none;
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
        <form class="form-container" on:submit|preventDefault={login}>
            <h3 class="login_text">로그인</h3>

            <div class="mb-3">
                <input type="text" bind:value={userId} class="form-control" placeholder="아이디를 입력하세요" required>
            </div>

            <div class="mb-3">
                <input type="password" bind:value={password} class="form-control" placeholder="비밀번호를 입력하세요" required>
            </div>

            <div class="mb-3 rememberId-div">
                <input type="checkbox" id="rememberId" bind:checked={rememberId}>
                <label for="rememberId" class="rememberId">아이디 저장</label>
            </div>

            {#if errorMessage}
                <p style="color: red;">{errorMessage}</p>
            {/if}

            <button type="submit" class="login_btn">로그인</button>

            <div class="separator my-3">또는</div>
            <!-- 카카오 로그인 버튼 -->
            <a id="kakao-login-btn" on:click|preventDefault={kakaoLogin} href="#">
                <img src="../src/assets/img/kakao_login.png" alt="카카오 로그인 버튼">
            </a>

            <div class="text-center mt-3">
                <span class="no-id">아이디가 없다면?&nbsp;</span><a use:link href="/Join" class="register-link">회원가입</a>
            </div>
        </form>
    </div>
</main>