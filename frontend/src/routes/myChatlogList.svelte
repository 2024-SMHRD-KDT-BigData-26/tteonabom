<script>
  import { onMount } from 'svelte';

  // 로그인한 사용자 혹은 현재 사용자의 USER_ID (실제 앱에서는 상태관리(store) 또는 라우트 파라미터로 처리)
  let userId = '';

  onMount(() => {
    const userData = localStorage.getItem('user'); // 'user' 키에서 가져오기
    if (userData) {
        try {
            const parsedUser = JSON.parse(userData);
            if (parsedUser.USER_ID) {
                userId = parsedUser.USER_ID; // USER_ID 값만 가져오기
                fetchUserChatrooms();
            } else {
                console.warn("localStorage에서 USER_ID를 찾을 수 없습니다.");
            }
        } catch (error) {
            console.error("localStorage 데이터 파싱 중 오류 발생:", error);
        }
    } else {
        console.warn("localStorage에서 user 데이터를 찾을 수 없습니다.");
    }
});


  // 백엔드에서 가져온 채팅방 목록을 저장할 변수
  let userChatrooms = [];
  let currentPage = 'visual_my';
  // 페이지네이션 갯수
  let currentSpotPage = 1;
  const itemsPerPage = 5;

  async function fetchUserChatrooms() {
    if (!userId) {
        console.error("❌ userId가 설정되지 않았습니다.");
        return;
    }

    try {
        // 1️⃣ 특정 사용자의 채팅 목록 가져오기
        console.log(`📢 [API 호출] 사용자 채팅 목록 가져오기: http://localhost:9000/chat/user/${userId}`);
        const userChatResponse = await fetch(`http://localhost:9000/chat/user/${userId}`);

        if (!userChatResponse.ok) {
            console.error("❌ 사용자의 채팅 목록을 불러오지 못했습니다.", userChatResponse.status);
            return;
        }

        const userChats = await userChatResponse.json();
        console.log("✅ [응답 확인] 사용자 채팅 목록:", userChats);

        if (userChats.length === 0) {
            console.warn("⚠️ 사용자의 채팅 목록이 비어 있습니다.");
            return;
        }

        // 2️⃣ 사용자가 만든 채팅방 목록 가져오기
        console.log(`📢 [API 호출] 사용자가 만든 채팅방 목록 가져오기: http://localhost:9000/crooms/user/${userId}`);
        const userRoomsResponse = await fetch(`http://localhost:9000/crooms/user/${userId}`);

        if (!userRoomsResponse.ok) {
            console.error("❌ 사용자가 만든 채팅방 목록을 불러오지 못했습니다.", userRoomsResponse.status);
            return;
        }

        const userRooms = await userRoomsResponse.json();
        console.log("✅ [응답 확인] 사용자가 만든 채팅방 목록:", userRooms);

        // 3️⃣ 사용자 채팅 목록에서 `croom_idx` 리스트 추출
        const userChatCroomIds = userChats.map(chat => chat.croom_idx);
        console.log("🔍 [매칭 작업] 사용자의 채팅방 번호 목록:", userChatCroomIds);

        // 4️⃣ 사용자가 만든 채팅방 목록에서 `croom_idx`가 있는 채팅방만 필터링
        userChatrooms = userRooms.filter(room => userChatCroomIds.includes(room.CROOM_IDX));
        console.log("✅ [최종 데이터] 사용자가 참여한 채팅방 목록:", userChatrooms);

    } catch (error) {
        console.error("❌ [오류 발생] 채팅방 데이터 불러오기 중 예외 발생:", error);
    }
}




  
  // 현재 페이지에 해당하는 데이터만 반환
  function getCurrentPageItems() {
    const startIndex = (currentSpotPage - 1) * itemsPerPage;
    const endIndex = currentSpotPage * itemsPerPage;
    return userChatrooms.slice(startIndex, endIndex);
  }

  // 페이지 변경 함수
  function changePage(page) {
    const totalPages = Math.ceil(userChatrooms.length / itemsPerPage);
    if (page > 0 && page <= totalPages) {
      currentSpotPage = page;
    }
  }
  



  // 상세 페이지로 이동하는 함수(예시, 라우터로 바꿔야함)
  function goToDetail(id) {
    window.location.href = `/#/MyChatlogView/${id}`;
  }
</script>

<style>
  /* 전체 영역 */
  .container {
    display: flex;
  }

  .main-content {
    overflow: hidden;
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
          <table class="table">
            <thead>
              <tr>
                <th class="idx-th">번호</th>
                <th class="title-th">채팅방 제목</th>
                <th class="date-th">생성일</th>
              </tr>
            </thead>
            <tbody>
              {#each userChatrooms as chatroom, index}
                <tr class="clickable" on:click={() => goToDetail(chatroom.CROOM_IDX)}>
                  <!-- API 응답 모델의 필드에 맞게 표시 -->
                  <td class="idx">{index + 1}</td>
                  <td class="title">{chatroom.CROOM_TITLE}</td>
                  <!-- 날짜는 JavaScript Date 객체를 활용해 포맷팅할 수 있음 -->
                  <td class="date">{new Date(chatroom.CREATED_AT).toISOString().split('T')[0]}</td>

                </tr>
              {/each}
              {#if userChatrooms.length === 0}
                <tr>
                  <td colspan="3" style="text-align: center;">채팅방이 없습니다.</td>
                </tr>
              {/if}
            </tbody>
          </table>

          <!-- 페이지네이션 -->
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm">
              <li class="page-item {currentSpotPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="javascript:void(0)" on:click={() => changePage(currentSpotPage - 1)}>&laquo;</a>
              </li>
              {#each Array(Math.ceil(userChatrooms.length / itemsPerPage)) as _, index}
                <li class="page-item {index + 1 === currentSpotPage ? 'active' : ''}">
                  <a class="page-link" href="javascript:void(0)" on:click={() => changePage(index + 1)}>
                    {index + 1}
                  </a>
                </li>
              {/each}
              <li class="page-item {currentSpotPage === Math.ceil(userChatrooms.length / itemsPerPage) ? 'disabled' : ''}">
                <a class="page-link" href="javascript:void(0)" on:click={() => changePage(currentSpotPage + 1)}>&raquo;</a>
              </li>
            </ul>
          </nav>           
        </div>
      </div>
    </div>
  </div>
</main>
