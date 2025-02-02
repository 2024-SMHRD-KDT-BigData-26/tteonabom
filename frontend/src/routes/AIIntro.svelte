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

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>나에게 꼭 맞는 여행정보를 알려드려요</p>
    <h1>여행AI</h1>
  </div>

  <!-- 여행AI 소개 컨텐츠 영역 -->
  <div class="content">
    <!-- ✅ 위쪽 영역 (챗봇 소개) -->
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

  <!-- ✅ 아래 영역 (버튼 + yellow_wave) -->
  <div class="bottom-section">
    <div class="footer">
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

<style>
  /* 기본 폰트 설정 */
  @font-face {
    font-family: "Paperlogy-4Regular";
    src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-4Regular.woff2")
      format("woff2");
    font-weight: 400;
    font-style: normal;
  }

  @font-face {
    font-family: "Paperlogy-6SemiBold";
    src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-6SemiBold.woff2")
      format("woff2");
    font-weight: 600;
    font-style: normal;
  }

  * {
    font-family: "Paperlogy-4Regular";
  }

  /* 전체 페이지 레이아웃 */
  .main-content {
    width: 100vw;
    min-height: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  /* content 영역 설정 */
  .content {
    width: 100vw;
    text-align: center;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0;
    padding: 0;
  }

  /* AI 소개 섹션 */
  .intro-section {
    text-align: center;
    margin-bottom: 20px; /* ✅ intro-section과 bottom-section 간격 줄임 */
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
    width: 400px;
    height: auto;
    display: block;
    margin-bottom: 10px;
  }

  /* 하단 섹션 (페이지 너비 전체) */
  .bottom-section {
    width: 100vw;
    height: 180px;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
  }

  /* 버튼 스타일 */
  .footer button {
    position: absolute;
    bottom: 70px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    z-index: 3;
  }

  .footer button:hover {
    background-color: #555;
  }

  /* yellow_wave 설정 (깨짐 방지) */
  .yellow-wave {
    width: 100%; /* 화면 너비에 꽉 차게 */
    height: auto; /* 높이는 자동으로 조정 (비율 유지) */
    object-fit: contain; /* 이미지 비율 유지 */
    position: absolute;
    bottom: 0;
    z-index: 1;
  }
</style>
