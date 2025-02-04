<style>
  :global(body), :global(html) {
    height: 100%;
    margin: 0;
    display: flex;
    flex-direction: column;
  }

  main {
    flex: 1 0 auto;
    display: flex;
    flex-direction: column;
    min-height: calc(100vh - 100px);
  }

  /* 화면 상단으로 딱 붙게 변경 */
  .content {
    flex: 1;
    padding: -100px;
    z-index: -1;         /* 다른 요소들보다 뒤에 배치 */
  }

  /* 배너 인디게이터 원형으로 변경 */
  .carousel-indicators > button {
  height: 7px;
  width: 7px;
  border-radius: 50%;
  margin-right: 10px;
  margin-bottom: 15px;
  }

  /* 배너 캡션 위치 조정 */
  .carousel-caption {
    padding-bottom: 40px;
  }

  /* 각 영역 타이틀 */
  .main-title {
    font-family: 'Paperlogy-6SemiBold';
    text-align: center; 
    font-size: 32px; 
    padding-top: 20px;
  }

  /* 행사정보 서브 타이틀 */
  .sub-title {
    font-family: 'Paperlogy-6SemiBold';
    text-align: center; 
    font-size: 24px; 
    color: #FF5D17;
  }

  /* 추천 여행지 컨테이너 */
.recommend-spot-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 50px;
}

/* 추천 여행지 목록 */
.recommend-spot-list {
  display: flex;
  gap: 50px; /* 아이템 간 간격 */
}

/* 추천 여행지 아이템 */
.recommend-spot-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 추천 여행지 이미지 */
.recommend-spot-img {
  width: 360px;
  max-height: 340px;
  object-fit: cover;
  max-width: 100%; /* 화면 크기에 맞게 너비 조정 */
  border-radius: 10px;
}

/* 추천 여행지 정보 전체 */
.recommend-spot-info {
  display: flex;
  align-items: center;
  width: 100%;
}

/* 추천 여행지 뱃지 */
.badge.bg-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  background-color: #FF5D17 !important;
}

/* 추천 여행지 카운트 */
.recommend-spot-count {
  display: flex;
  align-items: center;
  margin-left: auto;
  gap: 3px;
}

/* 추천 여행지 목록 타이틀 */
.recommend-spot-text {
  font-family: 'Paperlogy-6SemiBold';
  font-size: 16px;
  margin-left: 10px;
}

/* 추천 여행지 좋아요, 후기 이미지 */
.recommend-count-img {
  width: 18px;
  height: auto;
}

/* 추천 여행지 화살표 */
.recommend-spot-arrow-img {
  width: 40px;
  height: auto;
  cursor: pointer;
  transition: transform 0.3s ease;
}

/* 추천 여행지 화살표 호버 애니메이션 */
.recommend-spot-arrow-img:hover {
  cursor: pointer;
  transform: scale(1.1);
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  50% { transform: translateX(2px); }
  75% { transform: translateX(-2px); }
  100% { transform: translateX(0); }
}
  /* //////////////////////////////////////// */

  /* 이달의 행사정보 배경 */
  .fest-info {
    position: relative;
    left: 0;
    top: 0; 
    background: url('../assets/img/fest_home_bg.png') no-repeat center center;
    background-size: cover;
    width: 100vw; 
    height: 500px;
    margin-top: 10px;
  }

  /* 이달의 행사정보 카드 */
  .fest-card {
    cursor: pointer;
    overflow: hidden;
    transition: transform 0.3s;
  }

  /* 이달의 행사정보 이미지 */
  .fest-image {
    border: 1px solid #bbb;
  }

  /* 이달의 행사정보 제목 */
  h3 {
    font-family: 'Paperlogy-6SemiBold';
    font-size: 20px;
    margin-top: 16px;
  }

  /* 이달의 행사정보 기간, 장소 */
  p {
    font-size: 14px;
    margin: 2px;
  }

  /* 최신 후기 영역 */
  .masonry-grid {
  width: calc(413px * 3 + 30px * 2);
  margin-right: auto;
  padding-top: 40px;
  }

  /* 화면 너비가 1300px 이상일 때만 margin-left: 330px 적용 */
  @media (min-width: 1300px) {
    .masonry-grid {
      margin-left: 330px;
    }
  }

  /* 화면 너비가 900px 이상 1300px 미만일 때 (2열) */
  @media (max-width: 1299px) and (min-width: 900px) {
    .masonry-grid {
      width: calc(413px * 2 + 30px * 1); /* 2열일 때의 너비 */
      margin-left: auto;
      margin-right: auto;
    }
  }

  /* 화면 너비가 900px 미만일 때 (1열) */
  @media (max-width: 899px) {
    .masonry-grid {
      width: 413px; /* 1열일 때의 너비 */
      margin-left: auto;
      margin-right: auto;
    }
  }

  /* 후기 1개 영역 */
  .review-item {
    cursor: pointer;
    width: 413px;
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

  /* 스크롤 감지용 작은 영역 */
  .load-more-sentinel {
    height: 10px; 
  }

  /* 로딩 스피너 */
  .spinner-border {
    margin-bottom: 20px;
  }
</style>

<script>
  // 추천 여행지 목록 관련 
  import Carousel from 'svelte-carousel'

  import { RecommendSpotCarousel } from '../assets/js/recommend-spot.js';
  import { spots } from '../assets/js/recommend-spot-data.js';

  const carousel = new RecommendSpotCarousel(spots);
  let displayedSpots = carousel.getDisplayedSpots();

  // Spot 상세 페이지로 이동하는 함수
  function goToSpotDetail(spotId) {
    window.location.href = `/spot/${spotId}`; // 예: /spot/1
  }

  const prevItem = () => {
    displayedSpots = carousel.prevItem();
  };

  const nextItem = () => {
    displayedSpots = carousel.nextItem();
  };

  // 이달의 행사정보 관련
  import { thisMonthFests } from '../assets/js/this-month-fest.js';

  // 행사정보 클릭 시 링크로 이동
  function goToFestLink(link) {
    window.location.href = link;
  }

  // 최신 여행후기 관련
  import { onMount } from 'svelte';
  import Masonry from 'masonry-layout';
  import { loadMoreReviews, displayedReviews, loading } from '../assets/js/recent-review.js';

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

<main>
    <!-- 배너 인디게이터 영역 -->
    <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="3" aria-label="Slide 4"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="../src/assets/img/banner_001.png" class="d-block w-100" alt="배너1">
          <div class="carousel-caption d-none d-md-block">
            <h5>ChatGPT를 활용한</h5>
            <h5>올인원 여행 플랫폼 "떠나봄"</h5>
          </div>
        </div>
        <div class="carousel-item">
          <img src="../src/assets/img/banner_002.png" class="d-block w-100" alt="배너2">
          <div class="carousel-caption d-none d-md-block">
            <h5>여행AI 봄봄</h5>
            <p>나에게 꼭 맞는 여행정보를 찾아볼까요?</p>
          </div>
        </div>
        <div class="carousel-item">
          <img src="../src/assets/img/banner_004.png" class="d-block w-100" alt="배너3">
          <div class="carousel-caption d-none d-md-block">
            <h5>여행지</h5>
            <p>내가 원하는 여행 장소의 모든 것</p>
          </div>
        </div>
        <div class="carousel-item">
          <img src="../src/assets/img/banner_003.png" class="d-block w-100" alt="배너4">
          <div class="carousel-caption d-none d-md-block">
            <h5>행사·축제</h5>
            <p>지역의 행사와 축제를 찾아보세요</p>
          </div>
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
    <!-- 추천여행지 영역 -->
    <h1 class="main-title">추천 여행지</h1>
    <div class="d-flex justify-content-center align-items-center mt-5 gap-3">
      <!-- 왼쪽 화살표 -->
      <div on:click={prevItem}>
        <img 
          src="../src/assets/img/recommend_left_arrow.png" 
          alt="왼쪽 이동" 
          class="recommend-spot-arrow-img"
        >
      </div>
    
     <!-- 추천 여행지 목록 -->
      <div class="d-flex gap-3">
        {#each displayedSpots as spot, index}
          <div 
            class="d-flex flex-column align-items-center mb-3" 
            on:click={() => goToSpotDetail(spot.id)} 
            style="cursor: pointer;" 
          >
            <!-- 이미지 -->
            <img 
              src={spot.imgSrc} 
              alt={spot.location} 
              class="recommend-spot-img"
            >
            <!-- 정보 -->
            <div class="d-flex align-items-center w-100 mt-2">
              <span class="badge bg-primary">{spot.location}</span>
              <span class="recommend-spot-text ms-3">{spot.title}</span>
              <span class="d-flex align-items-center ms-auto gap-1">
                <img 
                  src="../src/assets/img/like_count.png" 
                  alt="좋아요 수" 
                  class="recommend-count-img"
                >
                {spot.likeCount}
                <img 
                  src="../src/assets/img/review_count.png" 
                  alt="후기 수" 
                  class="recommend-count-img"
                >
                {spot.reviewCount}
              </span>
            </div>
          </div>
        {/each}
      </div>
    
      <!-- 오른쪽 화살표 -->
      <div on:click={nextItem}>
        <img 
          src="../src/assets/img/recommend_right_arrow.png" 
          alt="오른쪽 이동" 
          class="recommend-spot-arrow-img"
        >
      </div>
    </div>
    <!-- 행사정보 영역 -->
    <div class="fest-info">
      &nbsp;
      <h1 class="main-title">이달의 행사정보</h1>
      <h2 class="sub-title">2025년 2월</h2>
      <div class="row fest-list content">
        {#each thisMonthFests as fest}
          <div class="col-md-3 mb-4">
            <div class="fest-card text-truncate" on:click={() => goToFestLink(fest.link)}>
              <img src={fest.image} alt={fest.title} class="img-fluid rounded-10 fest-image">
              <div class="fest-details">
                <h3>{fest.title}</h3>
                <p>기간: {fest.period}</p>
                <p>장소: {fest.location}</p>
              </div>
            </div>
          </div>
        {/each}
      </div>
      </div>
    <!-- 최신 여행후기 영역 -->
    <h1 class="main-title">최신 여행후기</h1>
    <div class="masonry-grid">
      {#each $displayedReviews as review}
        <div class="review-item" 
             on:click={() => goToEvent(review.REVIEW_IDX)}
             role="link"
             tabindex="0">
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
  </main>