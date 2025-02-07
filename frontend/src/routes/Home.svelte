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
  height: 340px;
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
  white-space: nowrap;      /* 한 줄로 표시 */
  overflow: hidden;         /* 넘치는 내용 숨김 */
  text-overflow: ellipsis;  /* ...으로 표시 */
  max-width: 200px;         /* 최대 너비 설정 */
  display: inline-block;    /* 크기 제한 적용을 위해 inline-block 사용 */
  vertical-align: middle;   /* 수직 정렬 */
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
    width: 300px;
    height: 172px;
    object-fit: cover;
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
// 페이지 이동을 위한 import
import { link } from "svelte-spa-router";
export let params;

// 추천 여행지 목록 관련 
import { onMount, tick } from 'svelte';
import Carousel from 'svelte-carousel';
import { RecommendSpotCarousel } from '../assets/js/recommend-spot.js';

let pois = [];
let carousel;
let displayedSpots = [];

// 최신 여행후기 관련
import Masonry from 'masonry-layout';
import { writable } from 'svelte/store';
import { timeAgo } from "../assets/js/timeAgo.js";

export const displayedReviews = writable([]); // 초기 빈 배열
export const loading = writable(false); // 데이터 로딩 상태 추적

// API에서 데이터를 가져와 설정
onMount(async () => {
  const res = await fetch('http://localhost:9000/pois');
  const allSpots = await res.json();

  // POI_URL이 유효한 것만 필터링 (디폴트 이미지 제외)
  pois = allSpots
    .filter(spot => spot?.POI_URL && spot?.POI_URL !== '../src/assets/img/default_image_r.png')
    .sort(() => 0.5 - Math.random())  // 랜덤으로 섞기
    .slice(0, 6); // 최대 6개만

  // 데이터를 불러온 후 캐러셀 생성
  carousel = new RecommendSpotCarousel(pois);
  displayedSpots = carousel.getDisplayedSpots();
});

// 이전 아이템으로 이동
const prevItem = () => {
  if (carousel) {
    displayedSpots = carousel.prevItem();
  }
};

// 다음 아이템으로 이동
const nextItem = () => {
  if (carousel) {
    displayedSpots = carousel.nextItem();
  }
};


  // 이달의 행사정보 관련
  let thisMonthFests = [];
  let festivals = [];

  let currentYear = new Date().getFullYear();
  let currentMonth = (new Date().getMonth() + 1).toString().padStart(2, "0"); // 1월 → "01" 형식

  async function fetchFestivals() {
    try {
      const response = await fetch("http://localhost:9000/festival");
      const data = await response.json();

      festivals = Array.isArray(data) ? data : [data];

      // ✅ 현재 연도/월과 일치하는 데이터만 필터링
      let filteredFests = festivals.filter((fest) => {
        let period = fest.FEST_PERIOD; // 예: "2025.02.01(목) ~ 2025.02.05(월)"
        let match = period.match(/^(\d{4})\.(\d{2})/); // 연도.월 추출 (예: "2025.02")

        if (match) {
          let festYear = match[1]; // "2025"
          let festMonth = match[2]; // "02"

          return festYear == currentYear && festMonth == currentMonth;
        }
        return false;
      });

      // ✅ 4개만 랜덤으로 선택
      thisMonthFests = getRandomItems(filteredFests, 4);

    } catch (error) {
      console.error("행사 정보를 불러오는 중 오류 발생:", error);
    }
  }

  // ✅ 배열에서 랜덤하게 N개 선택하는 함수
  function getRandomItems(array, count) {
    let shuffled = [...array].sort(() => 0.5 - Math.random()); // 배열 랜덤 섞기
    return shuffled.slice(0, count); // 앞에서 count개 선택
  }

  function goToFestLink(link) {
    if (link) window.location.href = link;
  }

  onMount(fetchFestivals);

  // 최신 여행후기 관련
  const fetchReviews = async () => {
    try {
      const response = await fetch("http://localhost:9000/reviews");
      if (!response.ok) {
        throw new Error("Failed to fetch reviews");
      }
      const data = await response.json();
      displayedReviews.set(data.slice(0, 6));
    } catch (error) {
      console.error("Error fetching reviews:", error);
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
          const nextIndex = $displayedReviews.length;
          const newReviews = data.slice(nextIndex, nextIndex + 6);

          displayedReviews.update((currentReviews) => [...currentReviews, ...newReviews]);
        } catch (error) {
          console.error("Error fetching more reviews:", error);
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
        {#each displayedSpots as spot}
          <div 
            class="d-flex flex-column align-items-center mb-3" 
          >
            <!-- 이미지 -->
            <a use:link href={`/SpotView/${spot.POI_IDX}`}>
            <img 
              src={spot?.POI_URL || '../src/assets/img/default_image_r.png'} 
              alt={spot.POI_REGION} 
              class="recommend-spot-img"
            >
            </a>
            <!-- 정보 -->
            <div class="d-flex align-items-center w-100 mt-2">
              <span class="badge bg-primary">{spot.POI_REGION}</span>
              <span class="recommend-spot-text">{spot.POI_NM}</span>
              <span class="d-flex align-items-center ms-auto gap-1">
                <img 
                  src="../src/assets/img/like_count.png" 
                  alt="좋아요 수" 
                  class="recommend-count-img"
                >
                {spot.POI_LIKES}
                <img 
                  src="../src/assets/img/review_count.png" 
                  alt="후기 수" 
                  class="recommend-count-img"
                >
                0
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
    <!-- 추천 여행지 끝 -->
    
    <!-- 이달의 행사정보 영역 -->
    <div class="fest-info">
      &nbsp;
      <h1 class="main-title">이달의 행사·축제</h1>
      <h2 class="sub-title">{currentYear}년 {currentMonth}월</h2>
      <div class="row fest-list content">
        {#each thisMonthFests as fest}
          <div class="col-md-3 mb-4">
            <div class="fest-card text-truncate">
              <a use:link href={`/FestView/${fest.FEST_IDX}`}>
                <img src={fest.FEST_URL} alt={fest.FEST_NM} class="img-fluid rounded-10 fest-image">
              </a>
              <div class="fest-details">
                <h3>{fest.FEST_NM}</h3>
                <p>기간: {fest.FEST_PERIOD}</p>
                <p>장소: {fest.FEST_ADDR}</p>
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
  </main>