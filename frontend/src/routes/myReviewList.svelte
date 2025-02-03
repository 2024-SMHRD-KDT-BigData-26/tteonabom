<script>
  // 비주얼존 배경명
  let currentPage = 'visual_my';

  // 비주얼존 CSS
  import '../assets/css/VisualZone.css';

  // 라우터
  import { link } from 'svelte-spa-router';
  import routes from '.././assets/js/routes.js';

  // 목록
  import { onMount } from 'svelte';
  import Masonry from 'masonry-layout';
  import { loadMoreReviews, displayedReviews, loading } from '../assets/js/recent-review.js';
  import { timeAgo } from "../assets/js/timeAgo.js";

  let masonryInstance;

  // Masonry 레이아웃 초기화
  onMount(() => {
    const grid = document.querySelector('.masonry-grid');
    masonryInstance = new Masonry(grid, {
      itemSelector: '.review-item',
      columnWidth: '.review-item',
      percentPosition: true
    });

    // IntersectionObserver 설정
    const observer = new IntersectionObserver(loadMoreReviews, {
      rootMargin: '50px',
      threshold: 1.0,
    });
    const sentinel = document.querySelector('#load-more');
    observer.observe(sentinel);
  });

  // 반응성 문법: displayedReviews가 변경될 때마다 Masonry 레이아웃 업데이트
  $: {
    if (masonryInstance) {
      masonryInstance.reloadItems();
      masonryInstance.layout();
    }
  }

  // 이미지 클릭 시 이동할 함수
  function goToEvent(reviewId) {
    window.location.href = `/#/reviewView/`; // ${reviewId}
  }

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
    height: 10px; 
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
                 on:click={() => goToEvent(review.REVIEW_IDX)}
                 role="link"
                 tabindex="0">
              
              <!-- 여행 후기 이미지 -->
              <img 
                src={review.FILE_NM} 
                alt="여행 후기 이미지" 
                class="review-image"
                on:load={() => {
                  if (masonryInstance) {
                    masonryInstance.reloadItems();
                    masonryInstance.layout();
                  }
                }}
              >
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
          </div>
        </div>

  </main>