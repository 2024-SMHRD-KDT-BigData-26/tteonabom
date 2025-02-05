<script>
  // 페이지 이동을 위한 import
  import { link } from "svelte-spa-router";

  // 비주얼존 배경명
  let currentPage = 'visual_spot';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  import { onMount } from 'svelte';

  // DB에서 여행지 데이터 가져오기
  let pois = [];
  
  onMount(async () => {
    const res = await fetch('http://localhost:9000/pois');
    let data = await res.json();

    // 이미지가 없는 항목 제외
    pois = data.filter(spot => spot.POI_URL && spot.POI_URL.trim() !== "");
  });

  // 지역 카테고리 선택
  let nationwideChecked = true;
  let regionsChecked = {
    seoul: false,
    incheon: false,
    daejeon: false,
    daegu: false,
    gwangju: false,
    busan: false,
    ulsan: false,
    gyeonggi: false,
    gangwon: false,
    chungbuk: false,
    chungnam: false,
    gyeongbuk: false,
    gyeongnam: false,
    jeonbuk: false,
    jeonnam: false,
    jeju: false,
    sejong: false
  };

  const regionNameMap = {
    seoul: "서울",
    incheon: "인천",
    daejeon: "대전",
    daegu: "대구",
    gwangju: "광주",
    busan: "부산",
    ulsan: "울산",
    gyeonggi: "경기",
    gangwon: "강원",
    chungbuk: "충북",
    chungnam: "충남",
    gyeongbuk: "경북",
    gyeongnam: "경남",
    jeonbuk: "전북",
    jeonnam: "전남",
    jeju: "제주",
    sejong: "세종"
  };

  // 전국 선택 시 다른 지역 해제 및 지역 선택 시 전국 해제
  function toggleNationwide() {
    if (nationwideChecked) {
      Object.keys(regionsChecked).forEach(region => regionsChecked[region] = false);
    }
  }

  function toggleRegion(region) {
    if (regionsChecked[region]) {
      nationwideChecked = false;
    }
  }

  // 페이지네이션을 위한 상태
  let currentPageNumber = 1; 
  const itemsPerPage = 6; // 한 페이지당 표시할 항목 수

  // 기본 정렬 순서
  let sortOption = 'latest';

  // 링크
  const goToView = (POI_IDX) => {
    link(`/SpotView/${POI_IDX}`);
  };

  // 지역 필터링, 순서 정렬
  $: filteredSpots = pois
  .filter(spot => {
    if (nationwideChecked) return true;
    return Object.keys(regionsChecked).some(region => 
      regionsChecked[region] && spot.POI_ADDR.includes(regionNameMap[region]));
  })
  .slice()
  .sort((a, b) => {
    if (sortOption === "latest" && a.CREATED_AT && b.CREATED_AT) return new Date(b.CREATED_AT) - new Date(a.CREATED_AT);
    if (sortOption === "popular") return b.POI_LIKES - a.POI_LIKES;
    return 0;
  });

  // 페이지네이션 함수
  function paginate(array, pageNumber, itemsPerPage) {
    return array.slice((pageNumber - 1) * itemsPerPage, pageNumber * itemsPerPage);
  }

  $: totalPages = Math.ceil(filteredSpots.length / itemsPerPage);
  $: visiblePois = filteredSpots.length > 0 ? paginate(filteredSpots, currentPageNumber, itemsPerPage) : [];

  // 페이지네이션 범위 계산
  $: paginationRange = (() => {
    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPageNumber - 2);
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    // 끝 부분에서 5개 유지
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
  })();
</script>

<style>
  /* 지역 필터링 체크박스 컬러 변경 */
  .form-check-input:checked {
    background-color: #FF5D17;
    border-color: #FF5D17;
  }

  /* 추천 여행지 컨테이너 */
  .spot-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1.25rem; /* gap-5 */
    width: 1300px;
    margin: 10px;
    padding-top: 15px;
  }

  /* 추천 여행지 목록 */
  .spot-list {
    display: flex;
    gap: 50px; /* 아이템 간 간격 */
  }

  /* 추천 여행지 아이템 */
  .spot-item {
    flex: 0 0 calc(33.333% - 1.25rem); /* 3개씩 배치 */
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* 추천 여행지 이미지 */
  .spot-img {
    width: 420px;
    height: 396px;
    object-fit: cover;
    max-width: 100%; /* 화면 크기에 맞게 너비 조정 */
    border-radius: 10px;
    cursor: pointer;
  }

  /* 추천 여행지 정보 전체 */
  .spot-info {
    display: flex;
    align-items: center;
    width: 100%;
    margin-top: 10px;
  }

  /* 추천 여행지 뱃지 */
  .badge {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    background-color: #FF5D17;
  }

  /* 추천 여행지 카운트 */
  .spot-count {
    display: flex;
    align-items: center;
    margin-left: auto;
    gap: 3px;
  }

  /* 추천 여행지 목록 타이틀 */
  .spot-text {
    font-family: 'Paperlogy-6SemiBold';
    font-size: 16px;
    margin-left: 10px;
  }

  /* 추천 여행지 좋아요, 후기 이미지 */
  .count-img {
    width: 18px;
    height: auto;
  }

  /* 페이지 네이션 */  
  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 0px;
    margin-bottom: 30px;
  }
  .page-link {
    cursor: pointer;
    padding: 0.5rem 0.75rem;
    border: 1px solid #dee2e6;
    color: #333;
    text-decoration: none;
  }
  .page-link:hover {
    background-color: #e9ecef;
  }
  .active .page-link {
    background-color: #333;
    color: white;
    border-color: #333;
  }
</style>
  
<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>원하는 지역의 여행장소를 찾아보세요</p>
    <h1>여행지</h1>
  </div>

  <!-- 여행지 목록 컨텐츠 영역 -->
  <div class="content">   
    <!-- 지역 필터링 시작 --> 
    <div class="container mt-4">
      <div class="p-2 border shadow-sm rounded" style="box-shadow: 0 0 4px rgba(0, 0, 0, 0.25);">
        <table class="table table-borderless mb-0">
          <tbody>
            <!-- 첫 번째 행: 전국 + 서울 ~ 광주 -->
            <tr>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="nationwide" bind:checked={nationwideChecked} on:change={toggleNationwide}>
                  <label class="form-check-label" for="nationwide">전국</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="seoul" bind:checked={regionsChecked.seoul} on:change={() => toggleRegion('seoul')}>
                  <label class="form-check-label" for="seoul">서울</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="incheon" bind:checked={regionsChecked.incheon} on:change={() => toggleRegion('incheon')}>
                  <label class="form-check-label" for="incheon">인천</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="daejeon" bind:checked={regionsChecked.daejeon} on:change={() => toggleRegion('daejeon')}>
                  <label class="form-check-label" for="daejeon">대전</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="daegu" bind:checked={regionsChecked.daegu} on:change={() => toggleRegion('daegu')}>
                  <label class="form-check-label" for="daegu">대구</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="gwangju" bind:checked={regionsChecked.gwangju} on:change={() => toggleRegion('gwangju')}>
                  <label class="form-check-label" for="gwangju">광주</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="busan" bind:checked={regionsChecked.busan} on:change={() => toggleRegion('busan')}>
                  <label class="form-check-label" for="busan">부산</label>
                </div>
              </td>
              <!-- 마지막 빈 5열 -->
              <td colspan="5"></td>
            </tr>
    
            <!-- 두 번째 행: 부산 ~ 세종 -->
            <tr>
              <td class="text-center">
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="ulsan" bind:checked={regionsChecked.ulsan} on:change={() => toggleRegion('ulsan')}>
                  <label class="form-check-label" for="ulsan">울산</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="gyeonggi" bind:checked={regionsChecked.gyeonggi} on:change={() => toggleRegion('gyeonggi')}>
                  <label class="form-check-label" for="gyeonggi">경기</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="gangwon" bind:checked={regionsChecked.gangwon} on:change={() => toggleRegion('gangwon')}>
                  <label class="form-check-label" for="gangwon">강원</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="chungbuk" bind:checked={regionsChecked.chungbuk} on:change={() => toggleRegion('chungbuk')}>
                  <label class="form-check-label" for="chungbuk">충북</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="chungnam" bind:checked={regionsChecked.chungnam} on:change={() => toggleRegion('chungnam')}>
                  <label class="form-check-label" for="chungnam">충남</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="gyeongbuk" bind:checked={regionsChecked.gyeongbuk} on:change={() => toggleRegion('gyeongbuk')}>
                  <label class="form-check-label" for="gyeongbuk">경북</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="gyeongnam" bind:checked={regionsChecked.gyeongnam} on:change={() => toggleRegion('gyeongnam')}>
                  <label class="form-check-label" for="gyeongnam">경남</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="jeonbuk" bind:checked={regionsChecked.jeonbuk} on:change={() => toggleRegion('jeonbuk')}>
                  <label class="form-check-label" for="jeonbuk">전북</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="jeonnam" bind:checked={regionsChecked.jeonnam} on:change={() => toggleRegion('jeonnam')}>
                  <label class="form-check-label" for="jeonnam">전남</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="jeju" bind:checked={regionsChecked.jeju} on:change={() => toggleRegion('jeju')}>
                  <label class="form-check-label" for="jeju">제주</label>
                </div>
              </td>
              <td class="text-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="sejong" bind:checked={regionsChecked.sejong} on:change={() => toggleRegion('sejong')}>
                  <label class="form-check-label" for="sejong">세종</label>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- 지역 필터링 끝 -->
    <!-- 게시물 수 / 정렬 시작-->
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <span>총 {filteredSpots.length}건</span>
        </div>
        <div>
          <select class="form-select" style="width: 100px;" bind:value={sortOption}>
            <option value="latest">최신순</option>
            <option value="popular">인기순</option>
          </select>
        </div>
      </div>
    </div>
    <!-- 여행지 목록 시작 -->
    <div class="spot-container">
      {#each visiblePois as poi}
      <div class="spot-item">
          <!-- 이미지 -->
          <a use:link href={`/SpotView/${poi.POI_IDX}`}>
            <img src={poi.POI_URL || "../src/assets/img/default_image_r.png"} alt="여행지 이미지" class="spot-img" />
          </a>
          <!-- 정보 -->
          <div class="spot-info">
            <span class="badge">{poi.POI_ADDR.slice(0, 2)}</span>
            <span class="spot-text">{poi.POI_NM}</span>
            <span class="d-flex align-items-center ms-auto gap-1">
              <img src="../src/assets/img/like_count.png" alt="좋아요 수" class="count-img" />
              0
              <img src="../src/assets/img/review_count.png" alt="후기 수" class="count-img" />
              0
            </span>
          </div>
        </div>
      {/each}
    </div>
    <!-- 여행지 목록 끝 -->
  </div>
 <!-- 페이지네이션 -->
<nav aria-label="Page navigation">
  <ul class="pagination pagination-sm">
    <!-- 처음 페이지 이동 -->
    <li class="page-item {currentPageNumber === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = 1}>&laquo;</a>
    </li>

    <!-- 이전 페이지 -->
    <li class="page-item {currentPageNumber === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = Math.max(1, currentPageNumber - 1)}>&lt;</a>
    </li>

    <!-- 페이지 번호 -->
    {#each paginationRange as page}
      <li class="page-item {page === currentPageNumber ? 'active' : ''}">
        <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = page}>{page}</a>
      </li>
    {/each}

    <!-- 다음 페이지 -->
    <li class="page-item {currentPageNumber === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = Math.min(totalPages, currentPageNumber + 1)}>&gt;</a>
    </li>

    <!-- 마지막 페이지 이동 -->
    <li class="page-item {currentPageNumber === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = totalPages}>&raquo;</a>
    </li>
  </ul>
</nav>
</main>