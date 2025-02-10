<script>
  // 비주얼존 배경명
  import { onMount } from 'svelte';
  import { push } from "svelte-spa-router"; // 페이지 이동을 위한 push 함수
  // 로그인 여부를 나타내는 변수
  let user = '';

  // 마운트 시 로컬스토리지에서 로그인 상태 확인
  onMount(() => {
    user = localStorage.getItem('user') || '';
  });

  let currentPage = "visual_AI";

  function navigateToChat() {
    // 로그인하지 않은 경우 alert 표시
    if (!user) {
      alert("로그인 후 이용 가능한 서비스입니다!");
      push("/login");
      return;
    }
    // 로그인 된 경우 페이지 이동
    push("/AIChat/");
  }

  // CSS 파일 import
  import "../assets/css/VisualZone.css";
</script>

<style>


  /* AI 소개 섹션 */
  .intro-section {
    margin-top: 20px;
    text-align: center;
  }

  .intro-section p {
    font-size: 16px;
    color: black;
  }

  .intro-section h1 {
    font-size: 24px;
    color: black;
  }

    /* 챗봇 이미지 */
    .chatbot-img {
    width: 500px;
    height: auto;
    display: inline-block;
    margin-top: 20px;
    margin-bottom: 10px;
    z-index: -1;
  }

  /* 버튼 스타일 */
  .button-div button {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
    color: white;
    border: none;
    padding: 12px 24px;
    margin-top: 50px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 20px;
    z-index: 3;
  }

  .button-div button:hover {
    background-color: #555;
  }

  .yellow-section {
    margin-top: -150px;
  }

  /* yellow_wave 설정 (깨짐 방지) */
  .yellow-wave {
  width: 100%; /* 화면 너비에 꽉 차게 */
  min-height: 150px;
  z-index: 1;

}

</style>

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>나에게 꼭 맞는 여행정보를 알려드려요</p>
    <h1>여행AI</h1>
  </div>

  <!-- 여행AI 소개 컨텐츠 영역 -->
  <div class="content">
    <!-- 위쪽 영역 (챗봇 소개) -->
    <div class="intro-section">
      <p>여행의 시작부터 끝까지<br />떠나봄의 AI와 함께하세요</p>
      <h1>AI가 당신의 완벽한 여행을 도와드립니다!</h1>

      <img
        src="/src/assets/img/chatbot_img.png"
        alt="챗봇 이미지"
        class="chatbot-img"
      />
    </div>
  </div>

  <!-- 아래 영역 (yellow_wave) -->
  
  <div class="yellow-section">
    <div class="button-div">
      <!-- 버튼 클릭 시 navigateToChat 함수 실행 -->
      <button on:click={navigateToChat}>
        <span>봄봄이랑 대화하러 가기</span>
      </button>
    </div>
    <img
      src="/src/assets/img/yellow_wave.png"
      alt="하단 배경 이미지"
      class="yellow-wave"
    />
  </div>
</main>


