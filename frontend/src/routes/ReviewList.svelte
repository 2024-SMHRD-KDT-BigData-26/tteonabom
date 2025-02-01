<script>
  // 비주얼존 배경명
  let currentPage = 'visual_review';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

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
    window.location.href = `/review/${reviewId}`; // 예시: /review/1
  }

</script>

<style>
  /* 등록 버튼 */
  .review-insert-btn {
    background-color: #333;
    width: 84px;
    margin: 20px 35px 20px 0;
    cursor: pointer;
  }

  .review-insert-btn:active {
    background-color: #555;
  }

  /* 후기 영역 */
  .masonry-grid {
  width: calc(427px * 3 + 30px * 2);
  margin-right: auto;
  margin-left: 0px;
  padding-top: 10px;
  }

  /* 후기 1개 영역 */
  .review-item {
    cursor: pointer;
    width: 427px;
    margin-bottom: 20px; 
    padding: 0 15px;
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

  /* 프로필 이미지 */
.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

/* 유저 정보 */
.review-info {
  display: flex;
  flex-direction: column;
}

.user-nick {
  font-weight: bold;
}

.created-at {
  color: gray;
  font-size: 14px;
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
        <p>여행을 다녀온 후기를 서로 공유해보세요</p>
        <h1>여행후기</h1>
      </div>

      <!-- 여행후기 상세 컨텐츠 영역 -->
      <div class="content">   
        <div class="d-flex justify-content-end">
          <button class="btn text-white review-insert-btn">등록</button>
        </div>
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
        
              <!-- 리뷰 정보 -->
              <div class="review-item-info">
                <img src={review.USER_PROFILE_IMG} alt="프로필 이미지" class="profile-img" />
                <div class="review-info">
                  <span class="user-nick">{review.USER_NICK}</span>
                  <span class="created-at">{timeAgo(review.CREATED_AT)}</span>
                </div>
              </div>
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