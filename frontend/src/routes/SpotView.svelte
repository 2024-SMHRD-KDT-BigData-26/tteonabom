<script>
  // 비주얼존 배경명
  let currentPage = 'visual_spot';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  // spot-data.js에서 데이터 불러오기
  import { spots } from "../assets/js/spot-data.js";

  import { onMount } from 'svelte';

// 좋아요 기능 관련
  let liked = false;
  let likeCount = 0;
  let userId = 1; // 실제로는 로그인한 사용자의 ID를 사용!!

  // 컴포넌트가 마운트될 때 좋아요 상태를 불러옵니다.
  onMount(async () => {
    const response = await fetch(`/api/likes?userId=${userId}`);
    const data = await response.json();
    liked = data.liked;
    likeCount = data.likeCount;
  });

  // 좋아요 버튼 클릭 시 호출되는 함수
  async function handleLike() {
    if (liked) return;

    const response = await fetch('/api/likes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userId }),
    });

    if (response.ok) {
      liked = true;
      likeCount += 1;
    }
  }

  // 이미지 확대
  export let image; // 이미지 URL을 props로 받습니다.

  let isModalOpen = false;

  // 모달 열기/닫기 함수
  function toggleModal() {
    isModalOpen = !isModalOpen;
  }

  // ESC 키를 눌렀을 때 모달 닫기
  onMount(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        isModalOpen = false;
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  });

////////////////////////////// 지도 관련 시작
  // 현재 여행지 ID (예: 1)
  let id = 1; // 실제로는 실제 여행지 ID를 사용!!

// ID에 해당하는 여행지 데이터 찾기
let spot = spots.find((spot) => spot.id === id);

// 카카오맵 API 초기화
let map;

onMount(() => {
  // 카카오맵 API 로드
  const script = document.createElement('script');
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=e2f8b444bceb65205ac527cd0f7f872a&autoload=false`;
  script.onload = () => {
    kakao.maps.load(() => {
      const container = document.getElementById('map');

      const selectedSpot = spots.find(spot => spot.id === id);

      if (selectedSpot) {
        const lat = selectedSpot.lat; // 선택된 여행지의 lat
        const lng = selectedSpot.lng; // 선택된 여행지의 lng
        
        const options = {
          center: new kakao.maps.LatLng(lat, lng), // 해당 여행지의 좌표를 사용
          level: 3,
        };

        const map = new kakao.maps.Map(container, options);

        // 모든 여행지에 마커 추가
        spots.forEach(spot => {
          const position = new kakao.maps.LatLng(spot.lat, spot.lng);
          const marker = new kakao.maps.Marker({
            position: position,
            title: spot.name,
          });
          marker.setMap(map);
        });
      } else {
        console.error('해당 ID에 맞는 여행지를 찾을 수 없습니다.');
      }
    });
  };
  
  document.head.appendChild(script);
});
////////////////////////////// 지도 관련 끝

////////////////////////////// 여행 후기 관련 시작
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
////////////////////////////// 여행 후기 관련 끝
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
    width: 100%;
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
          <!-- 상단: 카드로 위치, 이름, 좋아요 버튼 표시 -->
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center bg-transparent">
              <div class="spot-top-info">
                <div class="badge bg-primary">{spot.location}</div>
                <div class="card-title mb-0 spot-title ">{spot.name}</div>
              </div>
              <button on:click={handleLike} class="like-button">
                {#if liked}
                <img src="..\src\assets\img\like_on.png" alt="꽉찬하트" class="like-button-img">
                {:else}
                <img src="..\src\assets\img\like_off.png" alt="빈하트" class="like-button-img">
                {/if}
              </button>
            </div>
          <!-- 중간: 이미지와 표 형태 정보 -->
          <div class="card d-flex flex-row align-items-start card-body-div">
            <img src={spot.image} alt="여행지 이미지" class="card-img-top" on:click={toggleModal} />
            <div class="card-body">
              <table class="table table-hover">
                <tbody>
                  <tr>
                    <th scope="row" class="bg-light text-center">홈페이지</th>
                    <td><a href="{spot.url}" target="_blank">{spot.url}</a></td>
                  </tr>
                  <tr>
                    <th scope="row" class="bg-light text-center">주소</th>
                    <td>{spot.address}</td>
                  </tr>
                  <tr>
                    <th scope="row" class="bg-light text-center">문의 및 안내</th>
                    <td>{spot.tel}</td>
                  </tr>
                  <tr>
                    <th scope="row" class="bg-light text-center">이용시간</th>
                    <td>{spot.usetime}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- 하단: 좋아요 수와 후기 수 -->
            <div class="card-body d-flex gap-3 justify-content-end">
              <div>
                <img src="../src/assets/img/like_count.png" alt="좋아요 수" class="recommend-count-img">
                {spot.likes}
                <img src="../src/assets/img/review_count.png" alt="좋아요 수" class="recommend-count-img">
                {spot.reviews}
              </div>
            </div>
          </div>
        
          <!-- 상세 내용 -->
          <div class="card mb-4">
            <div class="card-body">
              <p class="card-text">
                {spot.overview}
              </p>
            </div>
          </div>
        
          <!-- 길찾기 라벨 및 카카오맵 -->
          <p class="card-title map-title">길찾기</p>
          <div class="card mb-4">
            <div class="card-body">
              <div id="map" class="map-container"></div>
            </div>
          </div>
        
          <!-- 한줄평(댓글) CRUD ---- 시간이 남으면 구현, 프론트작업 덜 됨
          <p class="card-title reply-title">한줄평 (10)</p>
          <div class="card mb-4">
            <div class="card-body">
              <textarea class="form-control comment-input" placeholder="한줄평을 입력하세요(최대100자)"></textarea>
              <button class="btn btn-primary mt-2">등록</button>
            </div>
          </div>
          -->

          <!-- 관련 후기 -->
          <p class="card-title reply-title">관련후기</p>
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
        </div>
    </div>

    <!-- 이미지 확대 모달 -->
    {#if isModalOpen}
      <div class="modal" on:click={toggleModal}>
        <img src={spot.image} alt="여행지 이미지 (원본 크기)" />
      </div>
    {/if}
    </main>