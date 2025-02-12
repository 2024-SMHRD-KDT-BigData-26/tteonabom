<script>
  import { onMount } from "svelte";

  let items = []; // DB에서 가져온 쇼핑 아이템 목록
  let sortedItems = []; // 정렬 및 필터링된 아이템 목록

  let currentPage = "visual_shopping";
  let currentSpotPage = 1; // 페이지네이션 상태
  const itemsPerPage = 9; // 한 페이지당 표시할 항목 수
  let selectedCategory = "전체"; // 선택된 카테고리 (기본값: 전체)
  let sortOption = "alphabetical"; // 기본 정렬: 가나다순
  

  // 로그인된 사용자 아이디 (localStorage에서 "user" 키의 데이터에서 USER_ID 추출)
  let userId = "";
  onMount(async () => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser && parsedUser.USER_ID) {
          userId = parsedUser.USER_ID;
        }
      } catch (error) {
        console.error("User parsing error:", error);
      }
    }
    // 먼저 쇼핑몰 데이터를 불러오고,
    await fetchShoppingData();
    // 로그인된 사용자가 있다면, 좋아요 기록도 불러와서 반영
    if (userId) {
      await fetchUserLikes();
    }
  });


  // 데이터 로딩: 쇼핑몰 목록 가져오기
  async function fetchShoppingData() {
    try {
      const res = await fetch("http://localhost:9000/shopping");
      if (!res.ok) {
        throw new Error("데이터를 불러오는 데 실패했습니다.");
      }
      items = await res.json();
      // 각 아이템에 liked, likeId 속성 추가 (초기값: false, null)
      items = items.map(item => ({ ...item, liked: false, likeId: null }));
      applyFilters();
    } catch (error) {
      console.error("에러 발생:", error);
    }
  }

  onMount(fetchShoppingData);

  // 사용자 좋아요 기록 불러오기
  async function fetchUserLikes() {
    try {
      const res = await fetch(`http://localhost:9000/like/user/${userId}`);
      if (!res.ok) {
        throw new Error("좋아요 데이터를 불러오는 데 실패했습니다.");
      }
      const likes = await res.json();  // 각 레코드: { LIKE_IDX, USER_ID, MALL_IDX, ... }
      const likedMallIds = likes.map(like => like.MALL_IDX);
      const likeIdMap = {};
      likes.forEach(like => {
        likeIdMap[like.MALL_IDX] = like.LIKE_IDX;
      });
      // items 배열에 사용자 좋아요 상태 반영
      items = items.map(item => {
        if (likedMallIds.includes(item.MALL_IDX)) {
          return { ...item, liked: true, likeId: likeIdMap[item.MALL_IDX] };
        }
        return item;
      });
      applyFilters();
    } catch (error) {
      console.error("좋아요 데이터 불러오기 오류:", error);
    }
  }

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
      { src: "/src/assets/img/fishhook_img.avif", name: "낚시" }
  ];

  // 카테고리 선택 함수
  function selectCategory(category) {
      selectedCategory = category;
      currentSpotPage = 1;
      applyFilters();
  }

  // 정렬 함수
function sortItems(items, sortType) {
    if (sortType === "alphabetical") {
        // 쇼핑몰 이름(MALL_NM) 기준 가나다순 정렬
        return [...items].sort((a, b) => a.MALL_NM.localeCompare(b.MALL_NM, "ko"));
    } else if (sortType === "likes") {
        // 좋아요 수(MALL_LIKES) 기준 내림차순 정렬
        return [...items].sort((a, b) => b.MALL_LIKES - a.MALL_LIKES);
    }
    return items;
}

  // 필터링 및 정렬 적용 함수
function applyFilters() {
    let filteredItems = selectedCategory === "전체"
        ? items
        : items.filter(item => item.CATEGORY === selectedCategory);
    
    sortedItems = sortItems(filteredItems, sortOption);
}

  // 현재 페이지에 표시할 항목 반환
  function getVisibleItems() {
      const startIndex = (currentSpotPage - 1) * itemsPerPage;
      return sortedItems.slice(startIndex, startIndex + itemsPerPage);
  }

  function changeSort(newSortOption) {
  sortOption = newSortOption;
  currentSpotPage = 1; // 정렬 시 1페이지로 돌아가게 설정
  applyFilters();
}

  const totalPages = () => Math.ceil(sortedItems.length / itemsPerPage);

  function changePage(page) {
      if (page >= 1 && page <= totalPages()) {
          currentSpotPage = page;
      }
  }
   // 좋아요 토글 기능 구현: 좋아요가 false면 1증가, true면 1감소하는 API 호출
   async function toggleLike(shop) {
    try {
      if (!shop.liked) {
        // 좋아요 추가: POST /like (USER_ID와 MALL_IDX 전송)
        const payload = { USER_ID: userId, MALL_IDX: shop.MALL_IDX };
        const response = await fetch("http://localhost:9000/like", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (!response.ok) {
          throw new Error("좋아요 추가 요청에 실패했습니다.");
        }
        const data = await response.json();
        shop.liked = true;
        shop.likeId = data.LIKE_IDX;
        // 쇼핑몰 좋아요 수 증가 (백엔드에서 /shopping/{MALL_IDX}/like를 별도로 관리하는 경우와 연동)
        // 여기서는 간단히 shop.MALL_LIKES 값을 증가시킵니다.
        shop.MALL_LIKES++;
      } else {
        // 좋아요 취소: DELETE /like/{LIKE_IDX}
        const response = await fetch(`http://localhost:9000/like/${shop.likeId}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" }
        });
        if (!response.ok) {
          throw new Error("좋아요 취소 요청에 실패했습니다.");
        }
        shop.liked = false;
        shop.likeId = null;
        shop.MALL_LIKES = Math.max(0, shop.MALL_LIKES - 1);
      }
      sortedItems = [...sortedItems];
    } catch (error) {
      console.error("좋아요 토글 실패:", error);
    }
  }

</script>

<main class="main-content">
  <div class={`visual-zone ${currentPage}`}>
    <p>여행용품이 필요하다면 이곳에서 구입해보세요</p>
    <h1>여행준비</h1>
  </div>

  <div class="content">
    <div class="img-bar">
      {#each categories as item}
      <div 
      class="shopping-img {selectedCategory === item.name ? 'selected' : ''}" 
      on:click={() => selectCategory(item.name)}>
          <img src={item.src} alt={item.name} class="main-img" />
          <span>{item.name}</span>
        </div>
      {/each}
    </div>

    <div class="items-header">
      <p class="item-count">총 {sortedItems.length}건</p>
      <div class="sort-container">
        <select class="form-select" on:change={(e) => changeSort(e.target.value)}>
          <option value="alphabetical">가나다순</option>
          <option value="likes">좋아요순</option>
        </select>
      </div>
    </div>

    <div class="card">
      {#each getVisibleItems() as shop}
        <div class="card-body">
          <div class="card-img">
            <a href={shop.MALL_URL} class="url" target="_blank">
              <img src={"src/assets/img/shopping/" + shop.MALL_IMG} alt="상품 이미지" />
            </a>
          </div>
          <hr class="divider" />
          <div class="card-content">
            <h5 class="card-category">#{shop.CATEGORY}</h5>
            <h5 class="card-title">{shop.MALL_NM}</h5>
            <div class="card-footer">
              <a href={shop.MALL_URL} class="url" target="_blank">{shop.MALL_URL}</a>
              <div class="like-section">
                <button class="like-btn" on:click={() => toggleLike(shop)}>
                  <img 
                    src={shop.liked ? "/src/assets/img/like_on.png" : "/src/assets/img/like_off.png"} 
                    alt="좋아요" />
                </button>
                <span class="like-count">{shop.MALL_LIKES}</span>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>

    <nav aria-label="Page navigation">
      <ul class="pagination pagination-sm">
        <li class="page-item {currentSpotPage === 1 ? 'disabled' : ''}">
          <button class="page-link" on:click={() => changePage(currentSpotPage - 1)}>&laquo;</button>
        </li>

        {#each Array(totalPages()).fill(0) as _, index}
          <li class="page-item {currentSpotPage === index + 1 ? 'active' : ''}">
            <button class="page-link" on:click={() => changePage(index + 1)}>{index + 1}</button>
          </li>
        {/each}

        <li class="page-item {currentSpotPage === totalPages() ? 'disabled' : ''}">
          <button class="page-link" on:click={() => changePage(currentSpotPage + 1)}>&raquo;</button>
        </li>
      </ul>
    </nav>
  </div>
</main>




<style>

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

  /* 화면 너비가 1340px 이하일 때 패딩 20px 적용 */
@media (max-width: 1340px) {
  .content {
    padding-right: 20px;
    padding-left: 20px;
  }
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

  /* 선택된 카테고리 버튼 스타일 (클릭한 버튼이 강조됨) */
.shopping-img.selected img {
  filter: brightness(0.1) grayscale(80%); /* 이미지 어둡게 */
  box-shadow: none; /* 기존 그림자 제거 */
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
    box-shadow: 0px 0px 6px rgba(255, 93, 23, 0.5);
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
  padding: 10px;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  overflow: hidden;
}

.card-img img {
  width: 80%;
  max-height: 50px;
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
    height: 250px;
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
    margin-bottom: -2px;
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

/* 쇼핑몰 이미지 중앙 정렬 */
.card-img a {
  display: flex;  /* a 태그 내부 요소 중앙 정렬 */
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
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
  width: 50px;
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
