<script>
  // 비주얼존 배경명
  let currentPage = 'visual_my';

  // 비주얼존 CSS
  import '../assets/css/VisualZone.css';

  // 회원가입 관련 기능(일단 넣어둔 것, 수정 필요할듯)
  import { createEventDispatcher } from 'svelte';
  import { handleProfileUpload, openFileDialog, handleSubmit } from '../assets/js/MyInfo.js';

  const dispatch = createEventDispatcher();
  
  let profilePreview = '';
  let profileUpload;
  let userId = 'user001'; // 아이디는 수정 불가능하게 출력만
  let currentPassword = '';
  let newPassword = '';
  let confirmNewPassword = '';
  let nickname = '';
  let errors = { passwordError: '', nickError: '' };

  async function submitToBackend() {
    if (newPassword && newPassword !== confirmNewPassword) {
      errors.passwordError = '새 비밀번호가 일치하지 않습니다.';
      return;
    }
    
    const payload = {
      currentPassword,
      newPassword,
      nickname
    };

    try {
      const response = await fetch('http://localhost:9000/api/myinfo', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('서버 오류 발생');
      }

      console.log('✅ 정보 변경 성공');
    } catch (error) {
      console.error('❌ 정보 변경 실패:', error);
    }
  }

  function onProfileUpload(event) {
    handleProfileUpload(event, (preview) => {
      profilePreview = preview;
    });
  }

  function checkNickname() {
    if (nickname.length < 1 || nickname.length > 8) {
      setErrors({ nickError: '닉네임은 1~8자 사이여야 합니다.' });
      return;
    }
    checkNickname(nickname, setErrors);
  }

  function handleCancel() {
    window.history.back();
  }

  // 상세 페이지로 이동하는 함수(예시, 라우터로 바꿔야함)
  function goToDetail(id) {
    window.location.href = `#/${id}`;
  }
</script>

<style>
  /* 전체 영역 */
  .container {
    display: flex;
  }

  /* 왼쪽 메뉴 전체 */
  .list-group {
    margin-top: 25px;
  }

  /* 왼쪽 메뉴 아이템 */
  .list-group-item {
    cursor: pointer;
    width: 200px;
  }

  .list-group-item.active {
    background-color: #333;
    border-color: #333;
  }
  
  /* 오른쪽 콘텐츠 */
  .my-content {
    flex: 1;
    margin-left: 25px;
    margin-top: 5px;
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

  .container {
    display: flex;
    width: 100%;
}

  /* 회원가입 폼 컨테이너 */
  .form-container {
      text-align: center; /* 내부 텍스트 가운데 정렬 */
      margin: 0 auto; /* 가로 중앙 정렬 */
      margin-top: 20px; 
      justify-content: center; /* 가로 중앙 정렬 */
      align-items: center; /* 세로 중앙 정렬 */
      width: 194%; 
      padding: 30px 30px 20px 30px; 
      border: 1px solid #D9D9D9; 
      border-radius: 10px; 
      background-color: #fff; 
  }

  /* 프로필 사진 업로드 섹션 */
  .profile_img {
      margin: 5px auto; /* 상단 여백 및 가운데 정렬 */
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

  /* 아이디 영역 */
  .ID {
      font-size: 14px; 
      font-weight: bold; 
      color: #333;
      margin-bottom: 20px;
  }
  /* 입력 필드 스타일 */
  .form-control {
      box-shadow: none; 
      height: 42px; /* 필드 높이 */
      width: 480px;
      font-size: 12px; /* 글자 크기 */
      padding: 10px; /* 내부 여백 */
      margin: auto;
  }

  .nick-update {
    width: 480px;
    margin: auto;
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
      justify-content: center; 
      margin: 20px auto 0 auto; /* 상단 여백 추가 및 가운데 정렬 */
      width: 194%;
  }

  /* 취소 버튼 */
  .cancel_btn {
      height: 42px; /* 입력 필드와 동일한 높이 */
      width: 84px;
      background-color: #ABB5BE; /* 기본 색상 */
      color: white;
      border: none;
      border-radius: 5px; /* 모서리를 둥글게 설정 */
      text-align: center; /* 텍스트 가운데 정렬 */
      margin-right: 20px; /* 오른쪽 여백 추가 */
      font-size: 14px;
  }

  /* 취소 버튼 호버 효과 */
  .cancel_btn:hover {
      background-color: #abb5beb6; /* 호버 시 색상 변경 */
  }

  /* 변경 버튼 */
  .update_btn {
      height: 42px; /* 입력 필드와 동일한 높이 */
      width: 84px;
      background-color: #333; /* 기본 색상 */
      color: white;
      border: none;
      border-radius: 5px; /* 모서리를 둥글게 설정 */
      text-align: center; /* 텍스트 가운데 정렬 */
      font-size: 14px;
    
  }

  /* 변경 버튼 호버 효과 */
  .update_btn:hover {
      background-color: #555; /* 호버 시 색상 변경 */
  }
  
</style>
  
    <main class="main-content">
      <!-- 비주얼 존 -->
      <div class={`visual-zone ${currentPage}`}>
        <p>나와 관련된 정보를 확인하세요</p>
        <h1>내여행</h1>
      </div>

      <!-- 내여행 > 채팅로그 목록 컨텐츠 영역 -->
      <div class="content">
        <div class="container">
          <!-- 왼쪽 메뉴 -->
          <div class="list-group">
            <div class="list-group-item" on:click={() => goToDetail('My')}>
              내 채팅로그
            </div>
            <div class="list-group-item" on:click={() => goToDetail('MyReview')}>
              내 여행후기
            </div>
            <div class="list-group-item active" on:click={() => goToDetail('MyInfo')}>
              내 정보변경
            </div>
          </div>
        
          <!-- 오른쪽 콘텐츠 -->
          <div class="my-content">
            <div class="container">
              <form on:submit|preventDefault={handleSubmit}>
                <div class="form-container">
                  <!-- 프로필 이미지 업로드 -->
                  <div class="profile_img" on:click={openFileDialog}>
                    {#if profilePreview}
                      <img 
                        id="profile-preview" 
                        src={profilePreview} 
                        alt="미리보기" 
                        style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; cursor: pointer;"
                      />
                    {:else}
                      <label for="profile-upload" id="profile-label" style="cursor: pointer;">
                        프로필 사진 변경
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
                  </div>
                  <div class="ID">{userId}</div>
              
                  <!-- 기존 비밀번호 입력 -->
                  <div class="mb-3">
                    <input
                      type="password"
                      bind:value={currentPassword}
                      class="form-control"
                      placeholder="기존 비밀번호를 입력하세요 (8~16자의 영문 대/소문자, 숫자)"
                      required
                    />
                  </div>
              
                  <!-- 새 비밀번호 입력 -->
                  <div class="mb-3">
                    <input
                      type="password"
                      bind:value={newPassword}
                      class="form-control"
                      placeholder="새 비밀번호를 입력하세요 (8~16자의 영문 대/소문자, 숫자)"
                      required
                    />
                  </div>
              
                  <!-- 새 비밀번호 확인 -->
                  <div class="mb-3">
                    <input
                      type="password"
                      bind:value={confirmNewPassword}
                      class="form-control"
                      placeholder="새 비밀번호를 다시 입력하세요"
                      required
                    />
                  </div>
              
                  <!-- 닉네임 변경 -->
                  <div class="mb-4 d-flex align-items-center nick-update">
                    <input
                      type="text"
                      bind:value={nickname}
                      class="form-control me-2"
                      placeholder="닉네임을 입력하세요 (1~8자)"
                      required
                    />
                    <button class="btn btn-outline-primary" type="button" on:click={checkNickname}>
                      중복확인
                    </button>
                  </div>
                </div>
              
                  <!-- 버튼 그룹 -->
                  <div class="btn-group">
                    <button type="button" class="cancel_btn" on:click={handleCancel}>취소</button>
                    <button type="submit" class="update_btn">변경</button>
                  </div>
              </form>
              
            </div>
          </div>
        </div>
      </div>
  </main>