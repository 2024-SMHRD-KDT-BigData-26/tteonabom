<script>
  import { shopItems, sortShopItems, filterItemsByCategory } from "../assets/js/ShoppingList.js";

  let currentPage = "visual_shopping";
  let sortOption = "likes"; // 기본 정렬: 좋아요순
  let currentSpotPage = 1; // 페이지네이션 상태
  const itemsPerPage = 9; // 한 페이지당 표시할 항목 수
  let selectedCategory = "전체"; // 선택된 카테고리 (기본값: 전체)

  // `shopItems`를 직접 변경하지 않고, 복사본을 사용해야 함
  let sortedShopItems = [...shopItems];

  // 카테고리 데이터
  const categories = [
    { src: "/src/assets/img/shopping_img.avif", name: "전체" },
    { src: "/src/assets/img/mountain_img.avif", name: "등산" },
    { src: "/src/assets/img/swimming_img.avif", name: "물놀이" },
    { src: "/src/assets/img/surfing_img.avif", name: "서핑" },
    { src: "/src/assets/img/swimsuit_img.avif", name: "수영복" },
    { src: "/src/assets/img/ski_img.avif", name: "스키" },
    { src: "/src/assets/img/travel_img.avif", name: "여행용품" },
    { src: "/src/assets/img/bicycle_img.avif", name: "자전거" },
    { src: "/src/assets/img/camera_img.avif", name: "카메라" },
    { src: "/src/assets/img/camping_img.avif", name: "캠핑" },
    { src: "/src/assets/img/fishhook_img.avif", name: "낚시" },
  ];

  // 카테고리 선택 함수
  function selectCategory(category) {
    selectedCategory = category;
    currentSpotPage = 1; // 카테고리 변경 시 페이지를 1로 초기화
    applyFilters(); // 필터링 적용
  }

  // 필터링 및 정렬 적용 함수
  function applyFilters() {
    let filteredItems = filterItemsByCategory(shopItems, selectedCategory); // 카테고리 필터링

    // 정렬 적용
    sortedShopItems = sortShopItems(filteredItems, sortOption);
  }

  // 현재 페이지에 표시할 항목 반환
  function getVisibleItems() {
    const startIndex = (currentSpotPage - 1) * itemsPerPage;
    return sortedShopItems.slice(startIndex, startIndex + itemsPerPage);
  }

  const totalPages = Math.ceil(sortedShopItems.length / itemsPerPage);

  // 페이지 변경 함수
  function changePage(page) {
    if (page >= 1 && page <= totalPages) {
      currentSpotPage = page;
    }
  }

  // 초기 필터링 적용
  applyFilters();
</script>

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>여행용품이 필요하다면 이곳에서 구입해보세요</p>
    <h1>여행준비</h1>
  </div>

  <div class="content">
    <!-- 이미지 바 -->
    <div class="img-bar">
      {#each categories as item}
        <div
          class="shopping-img"
          on:click={() => selectCategory(item.name)}
        >
          <img src={item.src} alt={item.name} class="main-img" />
          <span>{item.name}</span>
        </div>
      {/each}
    </div>

    <!-- 게시물 개수 + 정렬 -->
    <div class="items-header">
      <p class="item-count">총 {sortedShopItems.length}건</p>
      <div class="sort-container">
        <select
          class="form-select"
          on:change={(e) => changeSort(e.target.value)}
        >
          <option value="name">가나다순</option>
          <option value="likes">좋아요순</option>
        </select>
      </div>
    </div>

    <!-- 쇼핑몰 리스트 -->
    <div class="card">
      {#each getVisibleItems() as shop}
        <div class="card-body">
          <div class="card-img">
            <img src={shop.img} alt="샘플 이미지" />
          </div>
          <!-- 구분선 -->
          <hr class="divider" />
          <!-- 하단: card-content -->
          <div class="card-content">
            <h5 class="card-category">{shop.category}</h5>
            <h5 class="card-title">{shop.title}</h5>
            <div class="card-footer">
              <a href={shop.url} class="url" target="_blank">{shop.url}</a>
              <div class="like-section">
                <button class="like-btn">
                  <img src="/src/assets/img/heart.png" alt="좋아요" />
                </button>
                <span class="like-count">{shop.likes}</span>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>

    <!-- 페이지네이션 -->
    <nav aria-label="Page navigation">
      <ul class="pagination pagination-sm">
        <!-- 이전 페이지 버튼 -->
        <li class="page-item {currentSpotPage === 1 ? 'disabled' : ''}">
          <button
            class="page-link"
            on:click={() => changePage(currentSpotPage - 1)}>&laquo;</button
          >
        </li>

        <!-- 페이지 번호 버튼 -->
        {#each Array(totalPages).fill(0) as _, index}
          <li class="page-item {currentSpotPage === index + 1 ? 'active' : ''}">
            <button class="page-link" on:click={() => changePage(index + 1)}
              >{index + 1}</button
            >
          </li>
        {/each}

        <!-- 다음 페이지 버튼 -->
        <li
          class="page-item {currentSpotPage === totalPages ? 'disabled' : ''}"
        >
          <button
            class="page-link"
            on:click={() => changePage(currentSpotPage + 1)}>&raquo;</button
          >
        </li>
      </ul>
    </nav>
  </div>
</main>



<style>
  /* 기본 폰트 설정 */
  @font-face {
    font-family: "Paperlogy-4Regular"; /* 일반 폰트 */
    src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-4Regular.woff2")
      format("woff2");
    font-weight: 400;
    font-style: normal;
  }

  @font-face {
    font-family: "Paperlogy-6SemiBold"; /* 반굵은 폰트 */
    src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-6SemiBold.woff2")
      format("woff2");
    font-weight: 600;
    font-style: normal;
  }

  * {
    font-family: "Paperlogy-4Regular"; /* 기본 폰트 적용 */
  }

  /* 메인 컨테이너 */
  .main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 0; /* 화면 높이 100% */
    margin: 0 auto;
  }

  .content {
    width: 100%;
    max-width: 1300px;
    margin: 0 auto;
    min-height: calc(100vh - 390px);
    padding: 30px 0px 30px 0px;
    box-sizing: border-box;
    overflow: hidden;
  }

  /* 이미지 바 */
  .img-bar {
    display: flex;
    justify-content: center;
    gap: 15px; /* 이미지 간격 */
    width: 100%;
    max-width: 1300px;
    margin: 0 auto;
    margin-top: 25px;
  }

  .shopping-img {
    position: relative;
    width: 80px;
    height: 80px;
    border-radius: 50%; /* 원형 이미지 */
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
    cursor: pointer;
    transition: transform 0.3s ease;
  }

  .shopping-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    filter: brightness(0.5); /* 어두운 효과 */
  }

  .shopping-img span {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 0.9rem;
    white-space: nowrap;
    text-align: center;
  }

  .shopping-img:hover {
    transform: scale(1.1);
    filter: brightness(1);
    box-shadow: 0 4px 6px rgba(255, 93, 23, 0.5);
  }

  /* 쇼핑몰 리스트 */
  .shoppingmall-list {
    align-items: center;
    padding: 20px;
    margin-top: 20px;
  }

  /* 카드 레이아웃 */
  .card {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 3열 그리드 */
    gap: 20px;
    width: 100%;
    max-width: 1300px;
    margin: 0 auto;
    border: none;
  }
  .card-body {
    border: 1px solid #ddd;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    border-radius: 8px;
    background-color: #fff;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding: 0;
  }
  .card-img {
  flex: 1;
  width: 80%;
  height: 50%;
  display: flex;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  overflow: hidden;
}

.card-img img {
  width: 80%;
  height: 100%;
  object-fit: contain;
}

  .divider {
    width: 100%;
    border: 0;
    border-top: 1px solid #ddd;
    margin: 0;
  }

  /* 카드 내용 (아래쪽) */
  .card-content {
    flex: 1; /* 전체 높이의 50% */
    width: 100%;
    height: 50%; /* 높이를 반반 나눔 */
    padding-left: 20px;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  /* 카드 카테고리 */
  .card-category {
    margin-top: 20px;
    color: #ff7043;
    font-size: 14px;
    text-align: left;
  }
  .card-title {
    font-size: 18px;
    text-align: left;
  }
  /* 카드 푸터 */
.card-footer {
  display: flex;
  justify-content: space-between; /* 양쪽 정렬 */
  align-items: center;
  width: 100%;
  padding: 0;/* 좌우 여백 추가 */
  border: none;
  background: none;
  margin-top: -20px;
}

/* URL 링크 (왼쪽 정렬) */
.url {
  color: #999999;
  text-decoration: none;
  font-size: 12px;
  white-space: nowrap; /* 긴 URL이 줄바꿈되지 않도록 설정 */
  overflow: hidden;
  text-overflow: ellipsis; /* URL이 길 경우 '...' 처리 */
  flex-grow: 1; /* 가용 공간을 차지하여 균형 유지 */
  
}

/* 좋아요 섹션 (오른쪽 정렬) */
.like-section {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  flex-shrink: 0;
  margin-top: 0; /* 기존 -20px 제거하여 자연스럽게 배치 */
}

/* 좋아요 버튼 이미지 */
.like-btn img {
  width: 12px;
  height: 12px;
  cursor: pointer;
}


  /* 페이지 네이션 */
  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
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
  /* 게시물 개수 및 정렬 선택을 같은 줄에서 좌우 정렬 */
  .items-header {
    display: flex;
    justify-content: space-between; /* 양쪽 정렬 */
    align-items: center !important;
    width: 100%;
    max-width: 1300px;
    margin: 20px auto;
    padding: 10px 0;
  }

  /* 게시물 개수 스타일 */
  .item-count {
    font-size: 1rem;
    color: #333;
    margin-bottom: 0;
  }

  /* 정렬 선택 스타일 */
  .sort-container {
    display: flex;
    align-items: center;
  }

  .form-select {
    width: 120px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: none; /* 그림자 제거 */
    outline: none; 
  }

  /* 좋아요 섹션 */
  .like-section {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin: 10px;
    gap: 8px;
  }

  .like-count {
    font-size: 1rem;
    color: #333;
  }

  /* 좋아요 버튼 */
  .like-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .like-btn img {
    width: 20px;
    height: 20px;
    transition: transform 0.2s ease;
  }
</style>
