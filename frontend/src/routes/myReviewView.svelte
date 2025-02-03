<script>
  // 비주얼존 배경명
  let currentPage = 'visual_my';

  // 비주얼존 CSS
  import '../assets/css/VisualZone.css';


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
            <div class="list-group-item active" on:click={() => goToDetail('MyReview')}>
              내 여행후기
            </div>
            <div class="list-group-item" on:click={() => goToDetail('MyInfo')}>
              내 정보변경
            </div>
          </div>
        
          <!-- 오른쪽 콘텐츠 -->
          <div class="my-content">
            <h1>내 여행후기 내용 영역</h1>
          </div>
        </div>
      </div>
  </main>