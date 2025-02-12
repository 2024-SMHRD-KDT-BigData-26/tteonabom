<script>
  // 비주얼존 배경명
  let currentPage = "visual_spot";

  // 네비바 CSS
  import "../assets/css/VisualZone.css";

  export let params;

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

  // POI 상세 데이터를 저장할 변수
  let spot = null;

  // 좋아요 관련 상태
  let liked = false;
  let likeCount = 0;
  let likeId = null; // 사용자가 이 POI에 대해 생성한 좋아요 레코드의 id

  // 로그인된 사용자 ID (실제 로그인 시 localStorage에 저장된 "user" 객체에서 추출)
  let userId = "";

  // 모달 관련 상태 (이미지 확대)
  let isModalOpen = false;

  // onMount: 사용자 정보, POI 데이터, 좋아요 기록, Masonry, 모달 ESC 이벤트, 스크롤 최상단 이동
  onMount(async () => {
    // 1. 사용자 정보 불러오기
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

    // 2. POI 데이터 불러오기
    const poiRes = await fetch(`http://localhost:9000/pois/${params.POI_IDX}`);
    if (poiRes.ok) {
      spot = await poiRes.json();
      likeCount = spot.POI_LIKES; // POI의 초기 좋아요 수
      initMap(); // 카카오맵 초기화
    } else {
      console.error("POI 데이터를 불러오지 못했습니다:", poiRes.status, poiRes.statusText);
    }

    // 3. 해당 POI에 대한 좋아요 기록 불러오기
    if (spot && userId) {
      const resLikes = await fetch(`http://localhost:9000/like/poi/${spot.POI_IDX}`);
      if (resLikes.ok) {
        const likes = await resLikes.json();
        const userLike = likes.find(like => like.USER_ID === userId);
        if (userLike) {
          liked = true;
          likeId = userLike.LIKE_IDX;
        }
      } else {
        console.error("좋아요 데이터를 불러오지 못했습니다.");
      }
    }

    // 4. ESC 키 이벤트 등록 (모달 닫기)
    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        isModalOpen = false;
      }
    };
    window.addEventListener("keydown", handleKeyDown);

    // 5. 최상단 스크롤
    window.scrollTo(0, 0);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  // 좋아요 버튼 클릭 함수 (토글 기능)
  async function handleLike() {
    if (!liked) {
      // 좋아요 추가: POST /like 엔드포인트 사용
      const payload = { USER_ID: userId, POI_IDX: spot.POI_IDX };
      const response = await fetch("http://localhost:9000/like", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!response.ok) {
        console.error("좋아요 추가 실패");
        return;
      }
      const data = await response.json();
      liked = true;
      likeId = data.LIKE_IDX;
      likeCount++; // 좋아요 수 증가
    } else {
      // 좋아요 취소: DELETE /like/{LIKE_IDX} 엔드포인트 사용
      const response = await fetch(`http://localhost:9000/like/${likeId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" }
      });
      if (!response.ok) {
        console.error("좋아요 취소 실패");
        return;
      }
      liked = false;
      likeId = null;
      likeCount = Math.max(0, likeCount - 1);
    }
  }

  // 카카오맵 API 초기화 함수
  function initMap() {
    if (!spot) return;
    const script = document.createElement("script");
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=e2f8b444bceb65205ac527cd0f7f872a&autoload=false`;
    script.onload = () => {
      kakao.maps.load(() => {
        const container = document.getElementById("map");
        const lat = spot.LAT;
        const lng = spot.LON;
        const options = {
          center: new kakao.maps.LatLng(lat, lng),
          level: 3,
        };
        const map = new kakao.maps.Map(container, options);
        const position = new kakao.maps.LatLng(lat, lng);
        const marker = new kakao.maps.Marker({
          position: position,
          title: spot.POI_NM,
        });
        marker.setMap(map);
      });
    };
    document.head.appendChild(script);
  }

  // 모달 토글 함수 (이미지 확대)
  function toggleModal() {
    isModalOpen = !isModalOpen;
  }

  // 이미지 클릭 시 후기 상세 페이지 이동
  function goToEvent(reviewId) {
    window.location.href = `/review/${reviewId}`;
  }

  // 관련 후기
  const fetchReviews = async () => {
  try {
    const response = await fetch("http://localhost:9000/reviews");
    if (!response.ok) {
      throw new Error("Failed to fetch reviews");
    }
    const data = await response.json();

    // params.POI_IDX를 숫자로 강제로 변환
    const poiIndex = Number(params.POI_IDX);

    // 필터링된 리뷰 목록을 가져옴
    const filteredReviews = data.filter(review => {
      const reviewPoiIdx = Number(review.POI_IDX);
      return reviewPoiIdx === poiIndex;
    });

    // 필터링된 리뷰가 없으면 처리하지 않음
    if (filteredReviews.length === 0) {
      console.log("No reviews found for this POI.");
      return;
    }

    // filteredReviews를 사용하여 state 업데이트
    displayedReviews.set(filteredReviews.slice(0, 6));  // 처음 6개만 표시
    return filteredReviews.length;  // 후기 개수 리턴
  } catch (error) {
    console.error("Error fetching reviews:", error);
  }
};

// POI에 대한 후기 개수
let reviewCount = 0;

onMount(async () => {
  reviewCount = await fetchReviews();  // 후기 개수를 가져오기
});
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
        
        // params.POI_IDX를 숫자로 강제로 변환
        const poiIndex = Number(params.POI_IDX);

        // 필터링 로직 추가
        const filteredReviews = data.filter(review => {
          const reviewPoiIdx = Number(review.POI_IDX);
          return reviewPoiIdx === poiIndex;
        });

        // 이미 불러온 리뷰 수를 구함
        const nextIndex = $displayedReviews.length;

        // 필터링된 리뷰에서 다음 리뷰만 가져옴
        const newReviews = filteredReviews.slice(nextIndex, nextIndex + 6);

        if (newReviews.length > 0) {
          // 새로운 리뷰 추가
          displayedReviews.update((currentReviews) => [...currentReviews, ...newReviews]);
        }
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

<style>
  /* 상단 정보 전체 */
  .spot-top-info {
    display: flex;
    align-items: center;
    width: 100%;
  }

  /* 지역 뱃지 */
  .badge.bg-primary {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    background-color: #FF5D17 !important;
  }

  /* 여행지 명 */
  .spot-title {
    font-family: 'Paperlogy-6SemiBold';
    font-size: 20px;
    margin-left: 10px;
  }

  /* 좋아요 버튼 */
  .like-button {
    background: none;
    border: none;
    cursor: pointer;
  }

  /* 좋아요 버튼 이미지 */
  .like-button-img {
    width: 30px;
    height: auto;
  }

  /* 여행지 이미지 */
  .card-img-top {
    width: 50%;
    height: auto;
    max-width: 674px;
    max-height: 388px;
    padding: 15px 0px 0px 15px;
    cursor: pointer;
  }

  /* 이미지+표 테두리 */
  .card-body-div {
    border: none;
  }

  /* 추천 여행지 좋아요, 후기 이미지 */
  .recommend-count-img {
    width: 18px;
    height: auto;
  }

  /* 길찾기, 한줄평 타이틀 */
  .map-title, .reply-title {
    font-family: 'Paperlogy-6SemiBold';
    font-size: 14px;
    padding-bottom: 5px;
    padding-left: 2px;
  }

  /* 카카오맵 지도 */
  .map-container {
    width: 100%;
    height: 300px;
  }
  .comment-input {
    margin-bottom: 10px;
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

  /* 스크롤 감지용 작은 영역 */
  .load-more-sentinel {
    height: 10px; 
  }

  /* 로딩 스피너 */
  .spinner-border {
    margin-bottom: 20px;
  }

  /* 이미지 확대 모달 */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  /* 모달 내 이미지 */
  .modal img {
    max-width: 90%;
    max-height: 90%;
    border-radius: 8px;
  }

</style>

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>원하는 지역의 여행장소를 찾아보세요</p>
    <h1>여행지</h1>
  </div>

  <!-- 여행지 상세 컨텐츠 영역 -->
  <div class="content">
    <div class="container mt-4">
      <!-- 상단: POI 정보 및 좋아요 버튼 -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center bg-transparent">
          <div class="spot-top-info">
            <div class="badge bg-primary">
              {spot?.POI_REGION.slice(0, 2) || '-'}
            </div>
            {#if spot}
              <div class="spot-header">
                <div class="spot-title">{spot.POI_NM}</div>
              </div>
            {/if}
          </div>
          {#if spot}
            <button on:click={handleLike} class="like-button">
              {#if liked}
                <img src="/src/assets/img/like_on.png" alt="좋아요" class="like-button-img" />
              {:else}
                <img src="/src/assets/img/like_off.png" alt="좋아요" class="like-button-img" />
              {/if}
            </button>
          {/if}
        </div>
        <!-- 중간: POI 이미지 및 상세 정보 -->
        <div class="card d-flex flex-row align-items-start card-body-div">
          <img src={spot?.POI_URL || "../src/assets/img/default_image_o.png"} alt="여행지 이미지" class="card-img-top" on:click={toggleModal} />
          <div class="card-body">
            <table class="table table-hover">
              <tbody>
                <tr>
                  <th scope="row" class="bg-light text-center">주소</th>
                  <td>{spot?.POI_ADDR || '-'}</td>
                </tr>
                <tr>
                  <th scope="row" class="bg-light text-center">문의 및 안내</th>
                  <td>{spot?.POI_TEL || '-'}</td>
                </tr>
                <tr>
                  <th scope="row" class="bg-light text-center">이용시간</th>
                  <td>{spot?.POI_PERIOD || '-'}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- 하단: 좋아요 수 및 후기 수 -->
        <div class="card-body d-flex gap-3 justify-content-end">
          <div>
            <img src="../src/assets/img/like_count.png" alt="좋아요 수" class="recommend-count-img" />
            {likeCount}
            <img src="../src/assets/img/review_count.png" alt="후기 수" class="recommend-count-img" />
            {reviewCount}
          </div>
        </div>
      </div>

      <!-- 상세 내용 -->
      <div class="card mb-4">
        <div class="card-body">
          <p class="card-text">{spot?.POI_INFO || '-'}</p>
        </div>
      </div>

      <!-- 길찾기 및 카카오맵 -->
      <p class="card-title map-title">길찾기</p>
      <div class="card mb-4">
        <div class="card-body">
          <div id="map" class="map-container"></div>
        </div>
      </div>
      
      <!-- 관련 후기 -->
      {#if $displayedReviews.length > 0}
        <p class="card-title reply-title">관련후기</p>
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
      {/if}

      {#if $loading}
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      {/if}

      <!-- 이미지 확대 모달 -->
      {#if isModalOpen}
        <div class="modal" on:click={toggleModal}>
          <img src={spot?.POI_URL || "../src/assets/img/default_image_o.png"} alt="확대된 이미지" />
        </div>
      {/if}
    </div>
  </div>
</main>

