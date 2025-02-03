<script>
  // 비주얼존 배경명
  let currentPage = 'visual_fest';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  // 행사정보 데이터
  import { fests } from '../assets/js/fest-data.js';

  import { onMount } from 'svelte';

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
  // 현재 행사 ID (예: 1)
  let id = 1; // 실제로는 실제 행사 ID를 사용!!

  // ID에 해당하는 행사 데이터 찾기
  let fest = fests.find((fest) => fest.id === id);

  // 카카오맵 API 초기화
  let map;

  onMount(() => {
    // 카카오맵 API 로드
    const script = document.createElement('script');
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=e2f8b444bceb65205ac527cd0f7f872a&autoload=false`;
    script.onload = () => {
      kakao.maps.load(() => {
        const container = document.getElementById('map');

        const selectedFest = fests.find((fest) => fest.id === id);

        if (selectedFest) {
          const lat = selectedFest.lat; // 선택된 행사의 lat
          const lng = selectedFest.lng; // 선택된 행사의 lng

          const options = {
            center: new kakao.maps.LatLng(lat, lng), // 해당 행사의 좌표를 사용
            level: 3,
          };

          map = new kakao.maps.Map(container, options);

          // 모든 행사에 마커 추가
          fests.forEach((fest) => {
            const position = new kakao.maps.LatLng(fest.lat, fest.lng);
            const marker = new kakao.maps.Marker({
              position: position,
              title: fest.name,
            });
            marker.setMap(map);
          });
        } else {
          console.error('해당 ID에 맞는 행사를 찾을 수 없습니다.');
        }
      });
    };

    document.head.appendChild(script);
  });
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
  object-fit: contain; /* 이미지 비율 유지하면서 영역 안에 맞도록 설정 */
}

  /* 이미지+표 테두리 */
  .card-body-div {
    border: none;
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
        <!-- 상단: 카드로 위치, 이름, 좋아요 버튼 표시 -->
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center bg-transparent">
        <div class="spot-top-info">
          <div class="badge bg-primary">{fest.location.slice(0, 2)}</div>
          <div class="card-title mb-0 spot-title">{fest.title}</div>
        </div>
      </div>
    <!-- 중간: 이미지와 표 형태 정보 -->
    <div class="card d-flex flex-row align-items-start card-body-div">
      <img src={fest.image} alt="행사 이미지" class="card-img-top" on:click={toggleModal} />
      <div class="card-body">
        <table class="table table-hover">
          <tbody>
            <tr>
              <th scope="row" class="bg-light text-center">홈페이지</th>
              <td><a href={fest.url} target="_blank">{fest.url}</a></td>
            </tr>
            <tr>
              <th scope="row" class="bg-light text-center">주소</th>
              <td>{fest.address}</td>
            </tr>
            <tr>
              <th scope="row" class="bg-light text-center">문의 및 안내</th>
              <td>{fest.tel}</td>
            </tr>
            <tr>
              <th scope="row" class="bg-light text-center">행사기간</th>
              <td>{fest.period}</td>
            </tr>
            <tr>
              <th scope="row" class="bg-light text-center">공연시간</th>
              <td>{fest.playtime}</td>
            </tr>
            <tr>
              <th scope="row" class="bg-light text-center">행사장소</th>
              <td>{fest.eventplace}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="card-body d-flex gap-3 justify-content-end">
    </div>
  </div>
    <!-- 상세 내용 -->
    <div class="card mb-4">
      <div class="card-body">
        <p class="card-text">{fest.overview}</p>
      </div>
    </div>
    <!-- 길찾기 라벨 및 카카오맵 -->
    <p class="card-title map-title">길찾기</p>
    <div class="card mb-4">
      <div class="card-body">
        <div id="map" class="map-container"></div>
      </div>
    </div>
  </div>
</div>
  <!-- 이미지 확대 모달 -->
  {#if isModalOpen}
  <div class="modal" on:click={toggleModal}>
    <img src={fest.image} alt="행사 이미지 (원본 크기)" />
  </div>
  {/if}
</main>