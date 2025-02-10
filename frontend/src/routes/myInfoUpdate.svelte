<script lang="ts">
  import { onMount, tick } from 'svelte';
  import '../assets/css/VisualZone.css';

  // 로그인된 사용자 정보 (Login.svelte에서 "user" 키로 저장된 전체 사용자 정보에서 USER_ID 추출)
  let userId: string = '';
  // 기존 또는 새로 업로드된 프로필 사진 URL
  let profilePreview: string = '';
  // 파일 input 엘리먼트 참조
  let profileUpload: HTMLInputElement;



  let currentPage = 'visual_my';
  let newPassword = '';
  let confirmNewPassword = '';
  let nickname: string = '';
  let currentPassword = '';
  let errorMsg = '';
  let successMsg = '';
  let nicknameMsg = '';
  
  // 초기화된 닉네임을 저장할 변수
  let originalNickname: string = '';
  
  // Kakao 로그인 여부 (예: USER_ID가 "kakao_"로 시작하면 Kakao 로그인)
  let isKakao: boolean = false;

   // onMount에서 로컬스토리지에 저장된 사용자 정보를 불러옴
   onMount(() => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      const parsedUser = JSON.parse(storedUser);
      if (parsedUser) {
        if (parsedUser.USER_ID) {
          userId = parsedUser.USER_ID;
          // Kakao 로그인 여부 확인
          if (userId.startsWith("kakao_")) {
            isKakao = true;
          }
        }
        // 기존에 등록된 프로필 사진이 있다면 profilePreview에 할당
        if (parsedUser.USER_PROFILE_IMG.startsWith('/')) {
          profilePreview = `http://localhost:9000/images/${encodeURIComponent(parsedUser.USER_PROFILE_IMG)}`;
          console.log("프로필 이미지 URL:", profilePreview);
        } else {
          profilePreview = encodeURI(parsedUser.USER_PROFILE_IMG);
          console.log("프로필 이미지 URL:", profilePreview);
        }
        
        // 기존 닉네임을 자동 입력
        if (parsedUser.USER_NICK) {
          nickname = parsedUser.USER_NICK;
          originalNickname = parsedUser.USER_NICK;  // 기존 닉네임 저장
        }
      }
    }
    catch (error) {
      console.error("User parsing error:", error);
    }
  }
});
  
  // 프로필 이미지 업로드 핸들러
  async function onProfileUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files ? target.files[0] : null;
  if (file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:9000/api/upload", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("파일 업로드에 실패했습니다.");
      }

      const data = await response.json();
      // 서버가 반환한 fileUrl을 프로필 미리보기 이미지로 설정
      profilePreview = `${encodeURIComponent(data.fileUrl)}`;

      // Svelte의 tick을 사용하여 DOM 업데이트를 기다림
      await tick();

    } catch (error) {
      console.error("프로필 이미지 업로드 오류:", error);
      errorMsg = error.message;
    }
  }
}

  
  // 파일 업로드 창 열기
  function openFileDialog() {
    if (profileUpload) {
      profileUpload.click();
    }
  }

  // 폼 제출 시 실행되는 함수 (백엔드 PUT 요청)
  async function submitToBackend() {
    errorMsg = '';
    successMsg = '';

    // 닉네임을 변경하지 않았으면 기존 닉네임을 그대로 사용
    const finalNickname = nickname.trim() === '' ? originalNickname : nickname;

    if (!isKakao) {
        // 일반 로그인 사용자의 경우 새 비밀번호가 입력되었으면 일치 여부 확인
        if (newPassword && newPassword !== confirmNewPassword) {
            errorMsg = '새 비밀번호가 일치하지 않습니다.';
            return;
        }
    }

    // 회원정보 수정 API에 전달할 데이터 구성
    let updateData: any = {
        USER_NICK: finalNickname, // 변경된 닉네임 또는 기존 닉네임
    };

    // 일반 로그인 사용자인 경우에만 비밀번호 변경 필드 처리
    if (!isKakao && newPassword) {
        updateData.USER_PW = newPassword;
    }
    if (profilePreview) {
        updateData.USER_PROFILE_IMG = profilePreview;
    }

    try {
        const encodedUserId = encodeURIComponent(userId);
        const response = await fetch(`http://localhost:9000/api/myinfo?USER_ID=${encodedUserId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || '정보 수정에 실패했습니다.');
        }

        const result = await response.json();
        console.log('회원정보 수정 성공:', result);
        successMsg = '회원정보가 성공적으로 수정되었습니다.';

        // 서버에서 반환한 새 닉네임 값으로 `nickname`을 업데이트
        nickname = result.USER_NICK || finalNickname;  // 새로운 닉네임을 화면에 반영

        // 성공 후, 프로필 사진을 제외한 입력 필드 초기화
        currentPassword = "";
        newPassword = "";
        confirmNewPassword = "";
        
        // 로컬스토리지에 새로운 닉네임 저장
        const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
        storedUser.USER_NICK = nickname;
        localStorage.setItem('user', JSON.stringify(storedUser)); // 새 닉네임을 로컬스토리지에 저장

        // originalNickname을 새 닉네임으로 업데이트
        originalNickname = nickname;
        
    } catch (error) {
        console.error('회원정보 수정 실패:', error);
        errorMsg = error.message;
    }
}


  // 폼 제출 이벤트 핸들러
  function handleSubmit(event: Event) {
    event.preventDefault();
    submitToBackend();
  }

  // 닉네임 중복 확인 
  async function checkNickname() {
  // 닉네임이 입력되지 않았을 경우 처리
  if (!nickname || nickname.trim().length === 0) {
    nicknameMsg = '닉네임을 입력해주세요.';
    return;
  }

  // 닉네임이 이미 본인의 닉네임이라면 중복 메시지를 표시하지 않음
  if (nickname === userId) {
    nicknameMsg = '현재 사용 중인 닉네임입니다.';
    return;
  }

  try {
    // 프론트엔드 checkNickname 함수 내의 fetch 요청 수정
    const response = await fetch(`http://localhost:9000/api/check-nick?USER_NICK=${encodeURIComponent(nickname)}`);

    if (!response.ok) {
      throw new Error("닉네임 확인 중 오류가 발생했습니다.");
    }
    const data = await response.json();
    // 백엔드가 { available: true } 또는 { available: false }를 반환한다고 가정
    if (data.available) {
      nicknameMsg = '사용 가능한 닉네임입니다.';
    } else {
      nicknameMsg = '이미 사용중인 닉네임입니다. 다른 닉네임을 선택해주세요.';
    }
  } catch (error) {
    console.error("닉네임 중복 확인 실패:", error);
    nicknameMsg = "닉네임 중복 확인 중 오류가 발생했습니다.";
  }
}
 

  // 취소 버튼: 이전 페이지로 이동
  function handleCancel() {
    window.history.back();
  }

  // 상세 페이지로 이동하는 함수(예시, 라우터로 바꿔야함)
  function goToDetail(id) {
    window.location.href = `#/${id}`;
  }
</script>

<style>
  /* 기존 스타일 코드 그대로 사용 */
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
    margin: auto;
    display: block;
  }
  .container {
    display: flex;
    width: 100%;
  }
  /* 회원가입 폼 컨테이너 */
  .form-container {
    text-align: center;
    margin: 0 auto;
    margin-top: 20px;
    justify-content: center;
    align-items: center;
    width: 194%;
    padding: 30px 30px 20px 30px;
    border: 1px solid #D9D9D9;
    border-radius: 10px;
    background-color: #fff;
  }
  /* 프로필 사진 업로드 섹션 */
  .profile_img {
    margin: 5px auto;
    width: 120px;
    height: 120px;
    background-color: white;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
    color: #444;
    cursor: pointer;
    border: 2px solid #D9D9D9;
    position: relative;
  }
  /* 프로필 이미지 미리보기 */
  .profile_img img {
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    transition: 0.3s ease-in-out;
  }
  /* 숨겨진 파일 업로드 버튼 */
  .profile_img input[type="file"] {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
    z-index: 10;
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
    height: 42px;
    width: 480px;
    font-size: 12px;
    padding: 10px;
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
    margin-left: 5px;
    width: 100px;
    height: calc(2.5rem + 2px);
  }
  .btn-outline-primary:hover,
  .btn-outline-primary:active {
    background-color: #e65c00;
  }
  /* 버튼 그룹 */
.btn-group {
    display: flex;
    justify-content: center; 
    align-items: center;
    text-align: center;
    margin: 20px auto 0 auto; 
    width: 100%; 
}

  /* 취소 버튼 */
  .cancel_btn {
    height: 42px;
    width: 84px;
    background-color: #ABB5BE;
    color: white;
    border: none;
    border-radius: 5px;
    text-align: center;
    margin-right: 20px;
    font-size: 14px;
  }
  .cancel_btn:hover {
    background-color: #abb5beb6;
  }
  /* 변경 버튼 */
  .update_btn {
    height: 42px;
    width: 84px;
    background-color: #333;
    color: white;
    border: none;
    border-radius: 5px;
    text-align: center;
    font-size: 14px;
  }
  .update_btn:hover {
    background-color: #555;
  }

  /* 동일 닉네임 버튼 */
  .btn-outline-primary:disabled {
    background-color: #ABB5BE;
    color: white;
    cursor: not-allowed; /* 커서 모양 변경 */
}

  /* 출력 메시지 */
  .nickname-message, .error-message, .success-message {
  font-size: 12px;   /* 글자 크기 14px */

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
                  <!-- 기존 또는 새로 업로드된 프로필 이미지가 있을 경우 -->
                  <img 
                    id="profile-preview" 
                    src={`http://localhost:9000/images/${profilePreview}`}
                    alt="미리보기" 
                    style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; cursor: pointer;"
                  />
                {:else}
                  <!-- 프로필 이미지가 없을 경우 -->
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
              <!-- 사용자 아이디 (로그인한 사용자 아이디 표시) -->
              <div class="ID">{userId}</div>
            {#if !isKakao}
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
                  
                />
              </div>
              <!-- 새 비밀번호 확인 -->
              <div class="mb-3">
                <input
                  type="password"
                  bind:value={confirmNewPassword}
                  class="form-control"
                  placeholder="새 비밀번호를 다시 입력하세요"
                  
                />
              </div>
            {/if}
              <!-- 닉네임 변경 -->
              <div class="mb-4 d-flex align-items-center nick-update">
                <input
                  type="text"
                  bind:value={nickname}
                  class="form-control me-2"
                  placeholder="닉네임을 입력하세요 (1~8자)"
                />
                <button
                  class="btn btn-outline-primary"
                  type="button"
                  on:click={checkNickname}
                  disabled={nickname === originalNickname}
                >
                  중복확인
                </button>
              </div>
              <!-- 닉네임 중복 확인 결과 메시지 출력 -->
              {#if nicknameMsg}
                <div class="nickname-message">{nicknameMsg}</div>
              {/if}
               <!-- 에러 또는 성공 메시지 출력 -->
              {#if errorMsg}
               <div class="error-message">{errorMsg}</div>
              {/if}
              {#if successMsg}
                <div class="success-message">{successMsg}</div>
              {/if}
            <!-- 버튼 그룹 -->
            <div class="btn-group">
              <button type="button" class="cancel_btn" on:click={handleCancel}>취소</button>
              <button type="submit" class="update_btn">변경</button>
            </div>
            </div>
            
          </form>
        </div>
      </div>
    </div>
  </div>
</main>
