<script>
    import { isVisible, floatingBtnActions, scrollToTop } from '../assets/js/floatingBtn.js'; // 경로를 실제 파일에 맞게 수정
  
    // `isVisible` store 구독
    let buttonVisible;
    isVisible.subscribe(value => {
      buttonVisible = value; // `isVisible` 값에 따라 `buttonVisible`을 업데이트
    });
  </script>
  
  <style>
    .floating-btn {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 40px; /* 버튼 크기 */
      height: 40px; /* 버튼 크기 */
      background-image: url('../assets/img/floating_btn.png'); /* 이미지 경로 */
      background-size: cover; /* 이미지 크기에 맞게 조정 */
      background-position: center; /* 이미지가 버튼 안에서 중앙에 위치하도록 */
      border: none;
      border-radius: 50%; /* 원형 버튼 */
      cursor: pointer;
      display: none; /* 기본적으로 숨김 */
      transition: opacity 0.3s ease-in-out;
    }
  
    .floating-btn.visible {
      display: block; /* visible 클래스가 있을 때 버튼이 보이도록 설정 */
    }
  </style>
  
  <!-- 플로팅 버튼 -->
  <button
    class="floating-btn"
    class:visible={buttonVisible}
    use:floatingBtnActions
    on:click={scrollToTop}
  ></button>
  