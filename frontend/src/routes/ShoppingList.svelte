<script>
  // 비주얼존 배경명
  let currentPage = "visual_shopping";

  // JavaScript 파일 import
  import { setupShoppingList } from "../assets/js/ShoppingList.js";

  // onMount를 사용하여 컴포넌트가 로드될 때 실행
  import { onMount } from "svelte";
  onMount(() => {
    setupShoppingList();
  });

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

  // 샘플 쇼핑몰 데이터
  const shopItems = [
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle01.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크인",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
  ];
</script>
<style>
  /* 기본 폰트 설정 */
@font-face {
    font-family: 'Paperlogy-4Regular'; /* 일반 폰트 */
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-4Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
}

@font-face {
    font-family: 'Paperlogy-6SemiBold'; /* 반굵은 폰트 */
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-6SemiBold.woff2') format('woff2');
    font-weight: 600;
    font-style: normal;
}

* {
    font-family: 'Paperlogy-4Regular'; /* 기본 폰트 적용 */
}

/* 메인 컨테이너 */
.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh; /* 화면 높이 100% */
    margin: 0 auto;
}

.content {
    width: 100%;
    max-width: 1300px;
    margin: 0 auto;
    padding: 30px 0;
}

/* 이미지 바 */
.img-bar {
    display: flex;
    justify-content: center;
    gap: 15px; /* 이미지 간격 */
    width: 100%;
    max-width: 1300px;
    margin: 0 auto;
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

/* 정렬 버튼 */
.sort-btn {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    width: 100%;
    max-width: 1300px;
    margin: 20px auto;
}

.sort-text {
    background: none;
    border: none;
    padding: 0;
    font-size: 16px;
    color: #888;
    cursor: pointer;
}

.sort-btn.active {
    font-family: 'Paperlogy-6SemiBold';
    color: black;
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #fff;
    width: 100%;
    height: 200px;
    box-sizing: border-box;
}

/* 카드 이미지 */
.card-img {
    width: 100%;
    max-width: 100px;
    height: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.card-img img {
    width: 100%;
    height: auto;
    object-fit: contain;
}

/* 카드 내용 */
.card-content {
    text-align: left;
    justify-content: space-between;
}

/* 카드 카테고리 */
.card-category {
    color: #ff7043;
    font-size: 18px;
    text-align: left;
}
.card-title {
    font-size: 24px;
    text-align: left;
    
}

/* 카드 푸터 */
.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0;
    border: none;
    background: none;
}



/* 좋아요 섹션 */
.like-section {
    display: flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
}

.like-btn img {
    width: 12px;
    height: 12px;
    cursor: pointer;
}

/* 페이지네이션 */
.pagination {
    list-style: none;
    display: flex;
    justify-content: center;
    padding: 0;
    margin: 0;
    gap: 5px;
    margin-top: 20px;
}

.pagination .page-item {
    display: flex;
}

.pagination .page-link {
    text-decoration: none;
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    color: #6c757d;
    transition: background-color 0.3s, color 0.3s;
}

.pagination .page-link:hover {
    background-color: #e9ecef;
    color: black;
}

.pagination .page-item.active .page-link {
    background-color: #ff7043;
    color: white;
    border-color: #ff7043;
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

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>여행용품이 필요하다면 이곳에서 구입해보세요</p>
    <h1>여행준비</h1>
  </div>

  <!-- 여행준비 목록 컨텐츠 영역 -->
  <div class="content">
    <!-- 이미지 바 -->
    <div class="img-bar">
      {#each categories as item}
        <div class="shopping-img">
          <img src={item.src} alt={item.name} class="main-img" />
          <span>{item.name}</span>
        </div>
      {/each}
    </div>

    <!-- 쇼핑몰 리스트 -->
    <div class="shoppingmall-list">
      <div class="sort-btn">
        <button
          class="sort-text"
          on:click={() => setupShoppingList("alphabetical")}>가나다순</button
        >
        <button
          class="sort-text"
          on:click={() => setupShoppingList("likes")}>좋아요순</button
        >
      </div>

      <div class="card">
        {#each shopItems as shop}
          <div class="card-body">
            <div class="card-img">
              <img src={shop.img} alt="샘플 이미지" />
            </div>
            <div class="card-content">
              <h5 class="card-category">{shop.category}</h5>
              <h5 class="card-title">{shop.title}</h5>
              <!-- 좋아요와 URL을 한 줄에 정렬 -->

              <div class="card-footer">
                <a href={shop.url} class="url" target="_blank">{shop.url}</a>
                <div class="like-section">
                  <span class="like-count">{shop.likes}</span>
                  <button class="like-btn">
                    <img src="/src/assets/img/heart.png" alt="좋아요" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- 페이지네이션 -->
    <nav aria-label="Page navigation example">
      <ul class="pagination justify-content-center">
        <li class="page-item disabled">
          <a class="page-link" href="#">&lt;</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item"><a class="page-link" href="#">4</a></li>
        <li class="page-item">
          <a class="page-link" href="#">&gt;</a>
        </li>
      </ul>
    </nav>
  </div>
</main>