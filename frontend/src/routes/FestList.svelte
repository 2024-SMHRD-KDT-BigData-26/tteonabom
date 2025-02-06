<script>
  // 페이지 이동을 위한 import
  import { link } from "svelte-spa-router";

  // 비주얼존 배경명
  let currentPage = 'visual_fest';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  import { onMount } from 'svelte';

  // 년, 월 카테고리 선택
  let currentYear = new Date().getFullYear();
  let selectedMonth = '전체';
  const months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];

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


  // 전국 선택 시 다른 지역 해제
  function toggleNationwide() {
    if (nationwideChecked) {
      Object.keys(regionsChecked).forEach(region => {
        regionsChecked[region] = false;
      });
    }
    applyFilters();
  }

  // 다른 지역을 선택할 때 전국 해제
  function toggleRegion(region) {
    if (regionsChecked[region]) {
      nationwideChecked = false;
    }
    applyFilters();
  }

  // 행사정보 데이터
  let festivals = [];

  async function fetchFestivals() {
    try {
      const response = await fetch('http://localhost:9000/festival');
      const data = await response.json();
      festivals = Array.isArray(data) ? data : [data];
      applyFilters();
    } catch (error) {
      console.error('Error fetching festival data:', error);
    }
  }

  // 필터링된 행사 목록
  let filteredFests = [];
  let searchQuery = '';

  // 페이지네이션 관련
  let currentPageNumber = 1;
  const itemsPerPage = 8;

  // 기본 정렬 순서
  let sortBy = 'latest';

  // 링크
  const goToView = (FEST_IDX) => {
    link(`/FestView/${FEST_IDX}`);
  };

  // 필터 적용 함수
function applyFilters() {
  filteredFests = festivals.filter(fest => {
    const festYear = fest.FEST_PERIOD.substring(0, 4);
    const festMonth = fest.FEST_PERIOD.split('.')[1]?.padStart(2, '0');
    const festRegion = fest.FEST_LOC.substring(0, 2);

    // 검색 기능 추가
    if (searchQuery && !(
      fest.FEST_DESC.toLowerCase().includes(searchQuery.toLowerCase()) ||
      fest.FEST_ADDR.toLowerCase().includes(searchQuery.toLowerCase()) ||
      fest.FEST_NM.toLowerCase().includes(searchQuery.toLowerCase())
    )) {
      return false; // 검색 조건에 맞지 않으면 제외
    }

    // 년도 필터링
    if (festYear !== currentYear.toString()) return false;

    // 월 필터링 (전체가 아닌 경우)
    if (selectedMonth !== '전체') {
        const selectedMonthNumber = months.indexOf(selectedMonth) + 1;
        if (festMonth !== selectedMonthNumber.toString().padStart(2, '0')) return false;
    }

    // 전국이 체크된 경우 → 월 필터링만 적용하고 지역 필터링은 하지 않음
    if (nationwideChecked) return true;

    // 지역 필터링 (전국이 체크 안 된 경우)
    const selectedRegions = Object.keys(regionsChecked).filter(region => regionsChecked[region]);

    // 선택된 지역이 없으면 모든 데이터 표시
    if (selectedRegions.length === 0) return true;

    // fest.location이 선택된 지역과 일치하는지 확인
    return selectedRegions.some(region => festRegion.includes(regionNameMap[region]));
  });

  // 정렬 적용
  if (sortBy === 'latest') {
      filteredFests.sort((a, b) => new Date(b.FEST_PERIOD.split(' ~ ')[0]) - new Date(a.FEST_PERIOD.split(' ~ ')[0]));
  } else if (sortBy === 'ganada') {
      filteredFests.sort((a, b) => a.FEST_NM.localeCompare(b.FEST_NM, 'ko-KR'));
  }

  currentPageNumber = 1; // 필터 적용 시 첫 페이지로 이동
}


  // 페이지네이션 함수
  function paginate(array, pageNumber, itemsPerPage) {
    return array.slice((pageNumber - 1) * itemsPerPage, pageNumber * itemsPerPage);
  }

  // 상세 페이지로 이동하는 함수 (navigate 사용)
  function goToDetail(id) {
    window.location.href = `#/festView/`; // ${id} 추가 필요
  }

  // 정렬 변경 함수
  function changeYear(direction) {
    currentYear += direction;
    applyFilters();
  }

  function selectMonth(month) {
    selectedMonth = month;
    applyFilters();
  }

  function changeSort(event) {
    sortBy = event.target.value;
    applyFilters();
  }

  // 초기 필터 적용
  onMount(() => {
    fetchFestivals();
  });
</script>

<style>

  /* 월 필터링 */
  .all-month-select, .month-select {
    font-family: 'Paperlogy-6SemiBold';
    width: 70px;
    height: 70px;
    font-size: 16px;
    border: 1px solid #dee2e6;
    box-shadow: 0 0 3px rgba(0, 0, 0, 0.25);
  }

   /* 지역 필터링 체크박스 컬러 변경 */
   .form-check-input:checked {
    background-color: #FF5D17;
    border-color: #FF5D17;
  }

  /* 검색창 스타일 */
  .form-control {
    box-shadow: none;
    width: 200px;
    font-size: 14px;
    padding: 10px;
    margin: auto;
  }

  /* 순서 */
  .form-select {
    width: 120px !important;
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
    <p>원하는 지역의 행사·축제 정보를 찾아보세요</p>
    <h1>행사·축제</h1>
  </div>

  <!-- 행사·축제 목록 컨텐츠 영역 -->
  <div class="content">
    <div class="d-flex justify-content-center align-items-center my-3">
      <button class="btn btn-white me-3" on:click={() => changeYear(-1)}><strong>&lt;</strong></button>
      <h4 class="fw-bold">{currentYear}년</h4>
      <button class="btn btn-white ms-3" on:click={() => changeYear(1)}><strong>&gt;</strong></button>
    </div>

    <div class="d-flex justify-content-center flex-wrap">
      <button class="btn rounded-circle me-4 all-month-select {selectedMonth === '전체' ? 'btn-dark text-white' : 'btn-outline-dark'}" 
              on:click={() => selectMonth('전체')}>전체</button>
      {#each months as month}
        <button class="btn rounded-circle me-4 month-select {selectedMonth === month ? 'btn-dark text-white' : 'btn-outline-dark'}" 
                on:click={() => selectMonth(month)}>{month}</button>
      {/each}
    </div>

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
          <span>총 {filteredFests.length}건</span>
        </div>
        <div class="d-flex gap-2">
          <!-- 검색창 -->
          <div class="input-group">
            <input type="text" class="form-control" placeholder="찾을 내용을 입력해주세요" bind:value={searchQuery} on:input={applyFilters}>
          </div>
          <!-- 정렬 -->
          <select class="form-select" style="width: 100px;" on:change={changeSort}>
            <option value="latest">최신순</option>
            <option value="ganada">가나다순</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 행사 목록 시작 -->
    <div class="row fest-list content">
      {#each paginate(filteredFests, currentPageNumber, itemsPerPage) as festival}
        <div class="col-md-3 mb-4">
          <div class="fest-card text-truncate">
            <a use:link href={`/FestView/${festival.FEST_IDX}`}>
              <img src={festival.FEST_URL} alt={festival.FEST_NM} class="img-fluid rounded-10 fest-image">
            </a>
            <div class="fest-details">
              <h3>{festival.FEST_NM}</h3>
              <p>기간: {festival.FEST_PERIOD}</p>
              <p>장소: {festival.FEST_ADDR}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
    <!-- 행사 목록 끝 -->

    <!-- 페이지네이션 -->
    <nav aria-label="Page navigation">
      <ul class="pagination pagination-sm">
        <li class="page-item {currentPageNumber === 1 ? 'disabled' : ''}">
          <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = 1}>&laquo;</a>
        </li>
        {#each Array.from({ length: Math.ceil(filteredFests.length / itemsPerPage) }, (_, i) => i + 1) as page}
          <li class="page-item {page === currentPageNumber ? 'active' : ''}">
            <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = page}>{page}</a>
          </li>
        {/each}
        <li class="page-item {currentPageNumber === Math.ceil(filteredFests.length / itemsPerPage) ? 'disabled' : ''}">
          <a class="page-link" href="#" on:click|preventDefault={() => currentPageNumber = Math.ceil(filteredFests.length / itemsPerPage)}>&raquo;</a>
        </li>
      </ul>
    </nav>
  </div>
</main>