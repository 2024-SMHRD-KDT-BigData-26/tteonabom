<script>
  // 부트스트랩 CSS, JS
  import 'bootstrap/dist/css/bootstrap.min.css';
  import 'bootstrap/dist/js/bootstrap.min.js';

  // 기본 CSS
  import '../assets/css/Base.css';

  // 네비바 CSS
  import '../assets/css/Navbar.css';

  // 라우터
  import { link } from 'svelte-spa-router';

  // App.svelte에서 전달받은 isHomePage 값
  export let isHomePage = false;
</script>

<!-- 네비게이션 바 -->
<nav class="navbar">
  <div class="container-fluid navbar-content">
    <!-- 로고 -->
    <div class="d-flex align-items-center">
      <a use:link href="/" class="navbar-brand"><img src="..\src\assets\img\nav_logo.png" class="nav_logo" /></a>
    </div>

    <!-- 메뉴 -->
    <div class="d-flex justify-content-center flex-grow-1">
      <ul class="navbar-nav d-flex flex-row gap-3">
        <li class="nav-item" id="home">
          <!-- 홈 페이지일 때 nav-link의 클래스에 home-link를 추가 -->
          <a use:link href="/" class="nav-link {isHomePage ? 'home-link' : ''}">홈</a>
        </li>
        <li class="nav-item" id="AI">
          <a use:link href="/AI" class="nav-link">여행AI</a>
        </li>
        <li class="nav-item" id="shopping">
          <a use:link href="/Shopping" class="nav-link">여행준비</a>
        </li>
        <li class="nav-item" id="poi">
          <a use:link href="/Spot" class="nav-link">여행지</a>
        </li>
        <li class="nav-item" id="fest">
          <a use:link href="/Fest" class="nav-link">행사·축제</a>
        </li>
        <li class="nav-item" id="review">
          <a use:link href="/Review" class="nav-link">여행후기</a>
        </li>
        <!-- 비로그인 시 내여행 버튼 비노출-->
        <div id="mypage_menu">
          <li class="nav-item"><a use:link href="/My" class="nav-link" id="mypage">내여행</a></li>
        </div>
      </ul>
    </div>

    <!-- 로그인 버튼 -->
    <div class="d-flex align-items-center">
      <a use:link href="/Login" class="btn btn-primary login-btn">
        <img src="..\src\assets\img\login_btn_img.png" class="login_btn_img">로그인
      </a>
    </div>
    <!-- 로그아웃 버튼 -->
    <div class="d-flex align-items-center">
      <a href="#" class="btn btn-primary logout-btn">
        <img src="..\src\assets\img\logout_btn_img.png" class="logout_btn_img">로그아웃
      </a>
    </div>
  </div>
</nav>

<style>
  .navbar-nav .nav-link {
    text-decoration: none; /* 밑줄 제거 */
    color: rgb(0, 0, 0); /* 기본 메뉴 색상 */
    font-weight: 400; /* 기본 폰트 두께 */
    position: relative; /* 하단 바 위치를 위한 설정 */
    transition: all 0.3s ease; /* 부드러운 애니메이션 */
  }

  /* 마우스 호버 시 폰트 변경 */
  .navbar-nav .nav-link:hover {
    font-family: 'Paperlogy-6SemiBold';
    color: #000; 
  }
</style>
