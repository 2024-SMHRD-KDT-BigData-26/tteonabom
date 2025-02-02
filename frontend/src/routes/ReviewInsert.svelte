<script>
  // 비주얼존 배경명
  let currentPage = 'visual_review';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  // 라우터
  import { link } from 'svelte-spa-router';
  import routes from '.././assets/js/routes.js';

  // 여행지 자동완성 기능
  let query = ''; // 사용자 입력 값
  let results = []; // 자동완성 목록
  let isDropdownVisible = false; // 자동완성 목록 표시 여부
  let reviewContent = ''; // 후기 내용
  let reviewImage = null; // 후기 이미지

  // 고정된 여행지 목록(테스트용)
  const destinations = [
    "서울", "부산", "제주", "대구", "강릉", "전주", "광주", "춘천", "속초", "수원"
  ];

  // 여행지 자동완성 필터링 함수
  function filterDestinations() {
    if (!query) {
      results = [];
      isDropdownVisible = false;
      return;
    }
    results = destinations.filter(destination =>
      destination.toLowerCase().includes(query.toLowerCase())
    );
    isDropdownVisible = results.length > 0;
  }

  // 여행지 선택 시 입력값 설정
  function selectDestination(destination) {
    query = destination;
    results = [];
    isDropdownVisible = false;
  }

  // 입력값이 변경될 때마다 필터링 실행
  $: filterDestinations();  // `query`가 변경될 때마다 자동으로 호출

  // 랜덤한 3개의 여행지 목록 생성
  function getRandomDestinations() {
    // 여행지 목록에서 랜덤하게 3개를 선택
    let shuffled = [...destinations].sort(() => Math.random() - 0.3);
    return shuffled.slice(0, 3);
  }

  // 마우스 클릭 시 자동완성 목록을 랜덤하게 보여주기
  function handleFocus() {
    results = getRandomDestinations();
    isDropdownVisible = true;
  }

  // 폼 제출 시 유효성 검사
  function handleSubmit(event) {
    if (!destinations.includes(query)) {
      alert('목록에 있는 여행지를 선택해주세요.');
      event.preventDefault();
      return;
    }

    if (!reviewContent.trim()) {
      alert('후기 내용을 작성해주세요.');
      event.preventDefault();
      return;
    }

    if (!reviewImage) {
      alert('후기 이미지를 업로드해주세요.');
      event.preventDefault();
      return;
    }
  }

  // 취소 버튼 클릭 시 이전 페이지로 이동
  function goBack() {
    window.history.back();
  }
</script>

<style>
  h5 {
    font-family: 'Paperlogy-6SemiBold';
    margin-top: 15px;
    margin-bottom: 15px;
    font-size: 24px;
  }

  /* 자동완성 목록 스타일 */
  .autocomplete-item {
    cursor: pointer;
    padding: 8px;
    background-color: #ffffff;
  }

  .autocomplete-item:hover {
    background-color: #e9ecef;
  }
  
  /* 드롭다운 기준점 */
  .form-row {
  position: relative;
  }

  /* 드롭다운 메뉴 */
  .dropdown-menu {
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  position: absolute;
  width: calc(100% - 110px);  
  top: 100%;  /* 입력창 바로 아래에 위치 */
  left: 110px;  /* 라벨 너비 + 여백만큼 오른쪽으로 이동 */
  margin-top: 2px;  /* 입력창과의 간격 */
  background-color: white;  
  border: 1px solid #dee2e6;  
  border-radius: 4px;  
  box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
}

  .highlight {
    background-color: #fff3cd; /* 포커스된 항목 강조 */
  }

  /* 필수 항목 * 표시 */
  .required-label::before {
    content: "*";
    color: #FF5D17;
    margin-right: 5px;
  }

  /* 버튼 중앙 배치 */
  .button-container {
    display: flex;
    justify-content: center;
    gap: 20px;
  }

  /* 라벨과 입력창을 한 줄로 배치 */
  .form-row {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .form-row .form-label {
    margin-right: 10px;
    flex: 0 0 100px; /* 라벨의 너비를 고정 */
  }

  .form-row .form-control {
    flex: 1; /* 입력창은 가능한 공간을 모두 차지 */
  }

  /* 입력창 스타일 */
  input::placeholder, textarea::placeholder {
  font-size: 14px;
 	color: #abb4bd;
  }

  /* 파일 입력 버튼 텍스트 스타일 */
  input[type="file"]::file-selector-button {
  font-size: 14px;
  }

  /* 전체 파일 입력 스타일 */
  input[type="file"] {
  font-size: 14px;
  }

  /* 버튼 스타일 */
  .btn {
    padding: 10px 20px;
    font-size: 14px;
  }

  /* 취소 버튼 */
  .btn-cancel {
    background-color: #ABB5BE;
    color: #fff;
  }

  /* 등록 버튼 */
  .btn-submit {
    background-color: #333333;
    color: #fff;
  }
</style>

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>여행을 다녀온 후기를 서로 공유해보세요</p>
    <h1>여행후기</h1>
  </div>

  <!-- 여행후기 등록 컨텐츠 영역 -->
  <div class="content">
    <div class="d-flex justify-content-center align-items-center centered-container">
      <h5>여행후기 등록</h5>
    </div>
    <form on:submit|preventDefault={handleSubmit}>
      <!-- 여행지 선택 (자동완성) -->
      <div class="form-row">
        <label for="destination" class="form-label required-label">여행지 선택</label>
        <input
          id="destination"
          type="text"
          class="form-control"
          bind:value={query}
          placeholder="여행지 이름을 입력해 선택해주세요"
          on:focus={handleFocus}  
          on:input={filterDestinations} 
          on:blur={() => setTimeout(() => (isDropdownVisible = false), 200)} 
          autocomplete="off"
        />
        {#if isDropdownVisible && results.length > 0}
          <ul class="list-group mt-2 dropdown-menu">
            {#each results as result}
              <li
                class="list-group-item autocomplete-item"
                on:click={() => selectDestination(result)} 
              >
                {result}
              </li>
            {/each}
          </ul>
        {/if}
      </div>

      <!-- 후기 내용 -->
      <div class="form-row">
        <label for="reviewContent" class="form-label required-label">후기 내용</label>
        <textarea
          class="form-control"
          id="reviewContent"
          rows="8"
          placeholder="여행에 대한 후기를 작성해주세요"
          bind:value={reviewContent}
          required
        ></textarea>
      </div>

      <!-- 후기 이미지 -->
      <div class="form-row">
        <label for="reviewImage" class="form-label required-label">후기 이미지</label>
        <input
          class="form-control"
          type="file"
          id="reviewImage"
          accept="image/*"
          bind:files={reviewImage}
          required
        />
      </div>

      <!-- 버튼들 -->
      <div class="button-container">
        <button type="button" class="btn btn-cancel" on:click={goBack}>취소</button>
        <button type="submit" class="btn btn-submit">등록</button>
      </div>
    </form>
  </div>
</main>
