<script>
  // Navbar와 Footer 컴포넌트를 가져옴
  import Navbar from './components/Navbar.svelte';
  import Footer from './components/Footer.svelte';

  // 플로팅 버튼 함수
  import FloatingButton from './components/FloatingButton.svelte';

</script>

<div class="d-flex flex-column">
  <!-- 헤더 -->
  <Navbar />

  <!-- 메인 컨텐츠 영역 : 여기에 페이지 컨텐츠 넣기 -->
  <main>
    <Router {routes} />
  </main>

  <!-- 푸터 -->
  <Footer />

  <!-- 플로팅 버튼 -->
  <FloatingButton />
</div>

