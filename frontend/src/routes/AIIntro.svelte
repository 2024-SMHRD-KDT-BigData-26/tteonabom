<script>
  // 비주얼존 배경명
  let currentPage = "visual_AI";
  import { push } from "svelte-spa-router"; // 페이지 이동을 위한 push 함수

  function navigateToChat() {
    push("/AIChat/"); // AIChat 페이지로 이동
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


