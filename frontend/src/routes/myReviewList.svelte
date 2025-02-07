<script>
  // 비주얼존 배경명
  let currentPage = 'visual_my';

  // 비주얼존 CSS
  import '../assets/css/VisualZone.css';

  // 라우터
  import { link } from 'svelte-spa-router';
  import routes from '.././assets/js/routes.js';

  // 관련 임포트
  import { onMount, tick } from "svelte";
  import Masonry from 'masonry-layout';
  import { writable } from 'svelte/store';
  import { timeAgo } from "../assets/js/timeAgo.js";

  export const displayedReviews = writable([]); // 초기 빈 배열
  export const loading = writable(false); // 데이터 로딩 상태 추적

  let user = ''; // 로그인 상태 변수

  // 마운트 시 로컬스토리지에서 로그인 상태 확인
  onMount(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        user = JSON.parse(storedUser).USER_ID || ''; // USER_ID 추출
      } catch (error) {
        console.error("로그인 정보 파싱 오류:", error);
        user = '';
      }
    }
  });

  const fetchReviews = async () => {
  try {
    const response = await fetch("http://localhost:9000/reviews");
    if (!response.ok) {
      throw new Error("Failed to fetch reviews");
    }
    const data = await response.json();

    // ✅ 로그인한 사용자(user)의 USER_ID와 일치하는 리뷰만 필터링
    const filteredReviews = data.filter(review => review.USER_ID === user);

    // ✅ 필터링된 리뷰가 없을 경우 처리
    if (filteredReviews.length === 0) {
      displayedReviews.set([]); // 빈 배열 설정
      return;
    }

    displayedReviews.set(filteredReviews.slice(0, 6)); // 처음 6개만 표시

  } catch (error) {
  }
};


export const loadMoreReviews = (entries, observer) => {
  if (entries[0].isIntersecting) {
    loading.set(true); // 로딩 시작

    setTimeout(async () => {
      try {
        const response = await fetch("http://localhost:9000/reviews");
        if (!response.ok) {
          throw new Error("Failed to fetch reviews");
        }
        const data = await response.json();

        displayedReviews.update((currentReviews) => {
          const filteredReviews = data.filter(review => review.USER_ID === user);

          const currentCount = currentReviews.length;

          const newReviews = filteredReviews.slice(currentCount, currentCount + 6);

          if (newReviews.length === 0) {
            observer.disconnect(); // 더 이상 감지할 필요 없음
            return currentReviews;
          }

          return [...currentReviews, ...newReviews];
        });

      } catch (error) {
      } finally {
        loading.set(false);
      }
    }, 1000);
  }
};

  let masonryInstance;

  // Masonry 레이아웃 초기화
  onMount(async () => {
  await fetchReviews();
  await tick(); // DOM이 완전히 렌더링된 후 실행

  const grid = document.querySelector(".masonry-grid");
  masonryInstance = new Masonry(grid, {
    itemSelector: ".review-item",
    columnWidth: ".review-item",
    percentPosition: true,
  });

  // IntersectionObserver 설정
  const sentinel = document.querySelector("#load-more");
  if (sentinel) {
    const observer = new IntersectionObserver(loadMoreReviews, {
      rootMargin: "200px",
      threshold: 0.5,
    });
    observer.observe(sentinel);
  } else {
  }
});


  // 반응성 문법: displayedReviews가 변경될 때마다 Masonry 레이아웃 업데이트
  $: {
  if (masonryInstance) {
    masonryInstance.reloadItems();
    masonryInstance.layout();
  }
}

  // 상세 페이지로 이동하는 함수
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

  /* 후기 영역 */
  .masonry-grid {
  width: calc(355px * 3 + 30px * 2);
  margin-right: auto;
  margin-left: 0px;
  padding-top: 10px;
  }

  /* 후기 1개 영역 */
  .review-item {
    cursor: pointer;
    width: 358px;
    margin-bottom: 20px; 
    padding: 10px 15px 0px;
    transition: transform 0.2s;
  }

  /* 후기 1개 영역: 호버 시 */
  .review-item:hover {
    transform: translateY(-2px);
  }

  /* 후기 이미지 */
  .review-image {
    width: 100%;
    height: auto;
    border-radius: 10px;
    display: block;
  }

    /* 후기 정보 영역 */
  .review-item-info {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
  }

  /* 스크롤 감지용 작은 영역 */
  .load-more-sentinel {
    height: 30px; 
  }

  /* 로딩 스피너 */
  .spinner-border {
    margin-bottom: 20px;
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
          <!-- 여행후기 목록 -->  
    <div class="masonry-grid">
      {#each $displayedReviews as review}
        <div class="review-item" 
             role="link"
             tabindex="0">
          
          <!-- 여행 후기 이미지 -->
          <a use:link href={`/ReviewView/${review.REVIEW_IDX}`}>
          <img 
          src={`http://localhost:9000/images/${review.FILE_URL}`} 
          alt="여행 후기 이미지" 
          class="review-image"
          on:load={() => {
            if (masonryInstance) {
              masonryInstance.reloadItems();
              masonryInstance.layout();
            }
          }}
          on:error={(event) => {
            event.target.src = '../src/assets/img/default_image_o.png';  // 디폴트 이미지 경로
          }}
          />
          </a>
        </div>
      {/each}
    </div>

    <!-- 스크롤 감지 요소 -->
    <div id="load-more" class="load-more-sentinel"></div>

    {#if $loading}
      <div class="d-flex justify-content-center">
        <div class="spinner-border text-light" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    {/if}
  </div>
  </main>