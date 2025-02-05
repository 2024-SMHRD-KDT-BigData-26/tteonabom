<script>
  // 비주얼존 배경명
  let currentPage = 'visual_fest';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  import { onMount } from 'svelte';
  export let params;

  let festList = [];
  let festival = null; // festival 변수를 선언

  // 데이터 가져오기
  onMount(async () => {
    try {
      const res = await fetch(`http://localhost:9000/festival/${params.FEST_IDX}`);
      if (res.ok) {
        festival = await res.json();
        initMap(); // 데이터 로딩 후 지도 초기화
      } else {
        console.error('API 호출 실패:', res.status, res.statusText);
      }
    } catch (error) {
      console.error('API 요청 중 오류 발생:', error);
    }
  });

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
// 카카오맵 API 초기화 함수
function initMap() {
  if (!festival || !festival.LAT || !festival.LON) {
    console.error("지도 정보를 불러올 수 없습니다.");
    return;
  }

  // 카카오맵 스크립트가 이미 로드되었는지 확인
  if (!window.kakao || !window.kakao.maps) {
    const script = document.createElement('script');
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=e2f8b444bceb65205ac527cd0f7f872a&autoload=false`;
    script.onload = () => {
      kakao.maps.load(() => renderMap());
    };
    document.head.appendChild(script);
  } else {
    renderMap();
  }
}

// 지도 렌더링 함수
function renderMap() {
  const container = document.getElementById('map');

  if (!container) {
    console.error("지도 컨테이너를 찾을 수 없습니다.");
    return;
  }

  const lat = festival.LAT; // 축제 위도
  const lng = festival.LON; // 축제 경도

  const options = {
    center: new kakao.maps.LatLng(lat, lng),
    level: 3,
  };

  const map = new kakao.maps.Map(container, options);

  // 마커 추가
  const position = new kakao.maps.LatLng(lat, lng);
  const marker = new kakao.maps.Marker({
    position: position,
    title: festival.FEST_NM,
  });
  marker.setMap(map);
}
////////////////////////////// 지도 관련 끝


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

  /* 행사 명 */
  .spot-title {
    font-family: 'Paperlogy-6SemiBold';
    font-size: 20px;
    margin-left: 10px;
  }

  /* 행사 이미지 */
  .card-img-top {
  width: 100%; /* 부모 컨테이너에 맞게 크기 조정 */
  height: auto; /* 높이는 자동으로 비율을 맞춰서 설정 */
  max-width: 674px; /* 최대 가로 크기 */
  max-height: 388px; /* 최대 세로 크기 */
  padding: 15px 0px 0px 15px;
  cursor: pointer;
  object-fit: cover;
}

  /* 이미지+표 테두리 */
  .card-body-div {
    border: none;
  }

  /* 하단 여백 */
  .card-bottom {
    padding: 10px;
  }

  /* 길찾기 타이틀 */
  .map-title {
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

  /* 버튼 스타일 */
  .btn {
    padding: 10px 20px;
    font-size: 14px;
  }

  /* 목록 버튼 */
  .btn-secondary {
    background-color: #333333;
    color: #fff;
  }

  /* 목록 버튼을 중앙 배치 */
    .content .btn-container-back {
    text-align: center;
    margin-top: 20px;
  }
</style>
  
<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>원하는 지역의 행사·축제 정보를 찾아보세요</p>
    <h1>행사·축제</h1>
  </div>

  <!-- 행사·축제 상세 컨텐츠 영역 -->
  <div class="content">
    <div class="container mt-4">
      <!-- 상단: 카드로 위치, 이름 표시 -->
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center bg-transparent">
          <div class="spot-top-info">
            <div class="badge bg-primary">{festival?.FEST_LOC || '-'}</div>
            <div class="card-title mb-0 spot-title">{festival?.FEST_NM || '-'}</div>
          </div>
        </div>
        
        <!-- 중간: 이미지와 표 형태 정보 -->
        <div class="card d-flex flex-row align-items-start card-body-div">
          <img src={festival?.FEST_URL || "../src/assets/img/default_image_o.png"} alt="행사 이미지" class="card-img-top" on:click={toggleModal} />
          <div class="card-body">
            <table class="table table-hover">
              <tbody>
                <tr>
                  <th scope="row" class="bg-light text-center">주소</th>
                  <td>{festival?.FEST_ADDR || '-'}</td>
                </tr>
                <tr>
                  <th scope="row" class="bg-light text-center">문의 및 안내</th>
                  <td>{festival?.FEST_TEL || '-'}</td>
                </tr>
                <tr>
                  <th scope="row" class="bg-light text-center">행사기간</th>
                  <td>{festival?.FEST_PERIOD || '-'}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- 하단: 여백 영역 -->
        <div class="card-body d-flex justify-content-end card-bottom">
        </div>
      </div>

      <!-- 상세 내용 -->
      <div class="card mb-4">
        <div class="card-body">
          <p class="card-text">{@html festival?.FEST_DESC || '-'}</p>
        </div>
      </div>

      <!-- 길찾기 라벨 및 카카오맵 -->
      <p class="card-title map-title">길찾기</p>
      <div class="card mb-4">
        <div class="card-body">
          <div id="map" class="map-container"></div>
        </div>
      </div>

    <!-- 목록 버튼 -->
    <div class="btn-container-back">
      <button class="btn btn-secondary" on:click={() => window.history.back()}>목록</button>
    </div>


      <!-- 이미지 확대 모달 -->
      {#if isModalOpen}
      <div class="modal" on:click={toggleModal}>
        <img src={festival?.FEST_URL || "../src/assets/img/default_image_o.png"} alt="행사 이미지 (원본 크기)" />
      </div>
      {/if}

    </div>
  </div>
</main>
