<script>
  // 비주얼존 배경명
  let currentPage = 'visual_AI';

  // 비주얼존 CSS
  import '../assets/css/VisualZone.css';
</script>

<main class="main-content">
  <!-- 비주얼존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>나에게 꼭 맞는 여행정보를 알려드려요</p>
    <h1>여행AI</h1>
  </div>

  <!-- 여행AI 소개 컨텐츠 영역 -->
  <div class="content">
    <h2>AI 여행 플래너 소개</h2>
    <p>AI 여행 플래너는 사용자가 제공한 정보를 바탕으로 맞춤형 여행 계획을 추천합니다.</p>
    <p>당신의 여행을 보다 즐겁고, 효율적으로 만들어줄 여행 플래너입니다!</p>
  </div>
</main>

<style>
  .main-content {
    padding: 2em;
    text-align: center;
  }

  .visual-zone {
    background-color: #00bcd4;
    color: white;
    padding: 1em;
  }

  .content {
    margin-top: 2em;
  }
</style>
