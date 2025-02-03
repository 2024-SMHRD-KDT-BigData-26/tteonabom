<script>
    // 비주얼존 배경명
    let currentPage = 'visual_my';
  
    // 비주얼존 CSS
    import '../assets/css/VisualZone.css';

     // 예시 데이터 (목록)
  const chatLogs = [
    { id: 10, title: '여행지 추천', date: '2025.02.20' },
    { id: 9, title: '여행지 추천', date: '2025.02.20' },
    { id: 8, title: '일정 추천', date: '2025.02.20' },
    { id: 7, title: '일정 추천', date: '2025.02.20' },
    { id: 6, title: '여행지 추천', date: '2025.02.20' },
    { id: 5, title: '일정 추천', date: '2025.02.20' },
    { id: 4, title: '일정 추천', date: '2025.02.20' },
    { id: 3, title: '여행지 추천', date: '2025.02.20' },
    { id: 2, title: '일정 추천', date: '2025.02.20' },
    { id: 1, title: '일정 추천', date: '2025.02.20' },
  ];

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
    
    /* 목록 테이블 영역 */
    .table-container {
      padding: 20px;
    }
  
    .table {
      width: 100%;
      border-collapse: collapse;
    }
  
    .table th,
    .table td {
      padding: 10px;
    }

    /* 테이블 제목 */
    .title-th, .date-th {
      text-align: center;
    }

    /* 게시물 번호 영역 */
    .idx-th, .idx {
      width: 60px;
      text-align: center;
    }
    /* 저장일 영역 */
    .date, .date-th {
      width: 130px;
      text-align: center;
    }

    .title {
      cursor: pointer;
      text-align: left;
    }
  
    .table th {
      background-color: #f8f9fa;
      font-size: 14px;
    }
    
    /* 페이지 네이션 */  
    .pagination {
    display: flex;
    justify-content: center;
    margin-top: 0px;
    margin-bottom: 30px;
    }
    .page-link {
      cursor: pointer;
      padding: 0.5rem 0.75rem;
      border: 1px solid #dee2e6;
      color: #333;
      text-decoration: none;
    }
    .page-link:hover {
      background-color: #e9ecef;
    }
    .active .page-link {
      background-color: #333;
      color: white;
      border-color: #333;
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
              <div class="list-group-item active" on:click={() => goToDetail('My')}>
                내 채팅로그
              </div>
              <div class="list-group-item" on:click={() => goToDetail('MyReview')}>
                내 여행후기
              </div>
              <div class="list-group-item" on:click={() => goToDetail('MyInfo')}>
                내 정보변경
              </div>
            </div>
          
            <!-- 오른쪽 콘텐츠 -->
            <div class="my-content">
              <div class="table-container">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th class="idx-th">#</th>
                      <th class="title-th">제목</th>
                      <th class="date-th">저장일</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each chatLogs as { id, title, date }}
                      <tr>
                        <td class="idx">{id}</td>
                        <td class="title" on:click={() => goToDetail('MyChatlogView')}>{title}</td>
                        <td class="date">{date}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
          
                <!-- 페이지네이션 -->
                <nav aria-label="Page navigation">
                  <ul class="pagination pagination-sm">
                    <li class="page-item disabled">
                      <a class="page-link" href="/#/My" tabindex="-1" aria-disabled="true">&laquo;</a>
                    </li>
                    <li class="page-item active"><a class="page-link" href="/#/My">1</a></li>
                    <li class="page-item" aria-current="page">
                      <a class="page-link" href="/#/My">2</a>
                    </li>
                    <li class="page-item"><a class="page-link" href="/#/My">3</a></li>
                    <li class="page-item">
                      <a class="page-link" href="/#/My">&raquo;</a>
                    </li>
                  </ul>
                </nav>        
              </div>
            </div>
          </div>
        </div>
    </main>