<script>
  import { handleSubmit, handleProfileUpload, openFileDialog } from '../assets/js/Join.js';
  import { createEventDispatcher } from 'svelte';
  import '../assets/css/Join.css';

  const dispatch = createEventDispatcher();

  let profilePreview = '';
  let profileUpload;
  let userId = '';
  let password = '';
  let confirmPassword = '';
  let nickname = '';
  let errors = { idError: '', passwordError: '', nickError: '' };

  async function submitToBackend(data) {
    try {
        console.log("🔍 요청 데이터:", data);

        const payload = {
            userId: data.userId,
            password: data.password,
            nickname: data.nickname
        };

        const response = await fetch('http://localhost:9000/api/join', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const responseBody = await response.text();
        console.log("🔍 서버 응답:", responseBody);

        if (!response.ok) {
            throw new Error(`서버 오류: ${responseBody}`);
        }

        const result = JSON.parse(responseBody);
        console.log('✅ 회원가입 성공:', result);
    } catch (error) {
        console.error('❌ 회원가입 중 오류:', error);
    }
  }

  function onProfileUpload(event) {
    handleProfileUpload(event, (preview) => {
      profilePreview = preview;
    });
  }


  // 취소 버튼 클릭 시
  function handleCancel() {
    window.history.back(); // 이전 페이지로 이동
  }
</script>

<style>
  /* 아이디 및 닉네임 필드 너비 조정 */
  #userId,
  #nickname {
      width: 380px; /* 너비를 380px로 설정 */
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
  /* 회원가입 문구 */
  .join_text {
      margin-top: 10px;
      margin-bottom: 20px;
      font-family: 'Paperlogy-6SemiBold';
      font-size: 28px;
  }

  /* 회원가입 폼 컨테이너 */
  .form-container {
      text-align: center; /* 내부 텍스트 가운데 정렬 */
      margin: 0 auto; /* 가로 중앙 정렬 */
      margin-top: 50px; 
      justify-content: center; /* 가로 중앙 정렬 */
      align-items: center; /* 세로 중앙 정렬 */
      width: 540px; 
      height: 560px; 
      padding: 30px; 
      border: 1px solid #D9D9D9; 
      border-radius: 10px; 
      background-color: #fff; 
  }

  /* 프로필 사진 업로드 섹션 */
  .profile_img {
      margin: 20px auto; /* 상단 여백 및 가운데 정렬 */
      width: 120px; 
      height: 120px;
      background-color: white; 
      border-radius: 50%;
      display: flex; /* 내용 정렬을 위한 Flexbox */
      justify-content: center; /* 가로 중앙 정렬 */
      align-items: center; /* 세로 중앙 정렬 */
      font-size: 14px;
      color: #444; 
      cursor: pointer; /* 마우스 커서를 클릭 모양으로 변경 */
      border: 2px solid #D9D9D9; 
  }

  /* 프로필 이미지 미리보기 */
  .profile_img img {
      display: block; /* 블록 요소로 설정 */
      width: 100%; /* 부모 영역 너비 100% 채우기 */
      height: 100%; /* 부모 영역 높이 100% 채우기 */
      border-radius: 50%; 
      object-fit: cover; 
      transition: 0.3s ease-in-out; /* 부드러운 전환 효과 */
  }

  /* 숨겨진 파일 업로드 버튼 */
  .profile_img input[type="file"] {
      position: absolute; /* 프로필 이미지 위에 겹치도록 설정 */
      top: 0;
      left: 0;
      width: 100%; /* 부모 영역의 전체 너비 */
      height: 100%; /* 부모 영역의 전체 높이 */
      opacity: 0; /* 보이지 않도록 설정 */
      cursor: pointer; /* 클릭 가능한 커서 유지 */
      z-index: 10; /* 이미지보다 높은 z-index 설정 */
  }

  /* 입력 필드 스타일 */
  .form-control {
      box-shadow: none; 
      height: 42px; /* 필드 높이 */
      width: 480px;
      font-size: 12px; /* 글자 크기 */
      padding: 10px; /* 내부 여백 */
  }

  /* 중복확인 버튼 */
  .btn-outline-primary {
      font-size: 14px;
      background-color: #ff6600; 
      border: none; 
      color: white; 
      margin-left: 5px; /* 입력 필드와의 간격 추가 */
      width: 100px;
      height: calc(2.5rem + 2px); /* 입력 필드와 동일한 높이 */
  }

  .btn-outline-primary:hover, .btn-outline-primary:active {
      background-color: #e65c00;
  }



  /* 버튼 그룹 - 좌우 배치 및 전체 너비 설정 */
  .btn-group {
      display: flex; /* Flexbox 사용 */
      justify-content: space-between; /* 버튼을 좌우로 정렬 */
      width: 480px; /* 입력 필드와 동일한 너비 */
      margin: 20px auto 0 auto; /* 상단 여백 추가 및 가운데 정렬 */
  }

  /* 취소 버튼 */
  .cancel_btn {
      flex: 1; /* 버튼 너비 균등 분배 */
      height: 42px; /* 입력 필드와 동일한 높이 */
      background-color: #6c757d; /* 기본 색상 */
      color: white;
      border: none;
      border-radius: 5px; /* 모서리를 둥글게 설정 */
      text-align: center; /* 텍스트 가운데 정렬 */
      margin-right: 20px; /* 오른쪽 여백 추가 */
      font-size: 14px;
  }

  /* 취소 버튼 호버 효과 */
  .cancel_btn:hover {
      background-color: #5a6268; /* 호버 시 색상 변경 */
  }

  /* 회원가입 버튼 */
  .join_btn {
      flex: 1; /* 버튼 너비 균등 분배 */
      height: 42px; /* 입력 필드와 동일한 높이 */
      background-color: black; /* 기본 색상 */
      color: white;
      border: none;
      border-radius: 5px; /* 모서리를 둥글게 설정 */
      text-align: center; /* 텍스트 가운데 정렬 */
      font-size: 14px;
    
  }

  /* 회원가입 버튼 호버 효과 */
  .join_btn:hover {
      background-color: #333; /* 호버 시 색상 변경 */
  }
</style>

<!-- 가입 컨텐츠 영역 -->
<main class="content">
  <div class="container">
    <form 
      class="form-container" 
      on:submit|preventDefault={(e) => handleSubmit(
        e, 
        userId, 
        password, 
        confirmPassword, 
        nickname, 
        (newErrors) => errors = newErrors,
        submitToBackend
      )}
    >
      <h3 class="join_text">회원가입</h3>

      <!-- 프로필 이미지 -->
      <div class="profile_img">
        {#if !profilePreview}
          <label 
            for="profile-upload" 
            id="profile-label" 
            style="cursor: pointer;"
          >
            프로필 사진 선택
          </label>
        {/if}
        <input
          bind:this={profileUpload}
          id="profile-upload"
          name="profileImg"
          type="file"
          accept="image/*"
          style="display: none;"
          on:change={onProfileUpload}
        />
        {#if profilePreview}
          <img 
            id="profile-preview" 
            src={profilePreview} 
            alt="미리보기" 
            style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; cursor: pointer;"
            on:click={openFileDialog} 
          />
        {/if}
      </div>

      <!-- 아이디 입력 -->
      <div class="mb-3 d-flex align-items-center">
        <input
          type="text"
          bind:value={userId}
          class="form-control me-2"
          placeholder="아이디를 입력하세요 (5~10자의 영문 소문자, 숫자)"
          required
        />
        <button 
          class="btn btn-outline-primary" 
          type="button"
          on:click={() => {/* 아이디 중복 확인 로직 */}}
        >
          중복확인
        </button>
      </div>

      <!-- 비밀번호 입력 -->
      <div class="mb-3">
        <input
          type="password"
          bind:value={password}
          class="form-control"
          placeholder="비밀번호를 입력하세요 (8~16자의 영문 대/소문자, 숫자)"
          required
        />
      </div>

      <!-- 비밀번호 확인 -->
      <div class="mb-3">
        <input
          type="password"
          bind:value={confirmPassword}
          class="form-control"
          placeholder="비밀번호를 다시 입력하세요"
          required
        />
      </div>

      <!-- 닉네임 입력 -->
      <div class="mb-4 d-flex align-items-center">
        <input
          type="text"
          bind:value={nickname}
          class="form-control me-2"
          placeholder="닉네임을 입력하세요 (1~8자)"
          required
        />
        <button 
          class="btn btn-outline-primary" 
          type="button"
          on:click={() => {/* 닉네임 중복 확인 로직 */}}
        >
          중복확인
        </button>
      </div>

      <!-- 버튼 그룹 -->
      <div class="btn-group">
        <button 
          type="button" 
          class="cancel_btn"
          on:click={handleCancel}
        >
          취소
        </button>
        <button type="submit" class="join_btn">회원가입</button>
      </div>
    </form>
  </div>
</main>
