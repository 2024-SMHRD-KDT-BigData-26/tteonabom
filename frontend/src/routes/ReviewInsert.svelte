<script>
  import { onMount } from "svelte";

  // 로그인 상태 관리
  let user = '';

  // 마운트 시 로컬스토리지에서 로그인 상태 확인 
  onMount(() => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      user = JSON.parse(storedUser).USER_ID || ''; // USER_ID 추출
    } catch (error) {
      console.error("로그인 정보 파싱 오류:", error);
      user = '';
    }
  }

  // localStorage 변경 감지
  window.addEventListener('storage', (event) => {
    if (event.key === 'user' && event.newValue) {
      try {
        user = JSON.parse(event.newValue).USER_ID || ''; // USER_ID 추출
      } catch (error) {
        console.error("로그인 정보 업데이트 오류:", error);
        user = '';
      }
    }
  });
});

  // 여행지 자동완성 기능
  let destinations = []; // 여행지 목록
  let pois = []; // POI 데이터 저장
  let query = ''; // 사용자 입력 값
  let results = []; // 자동완성 목록
  let isDropdownVisible = false; // 자동완성 목록 표시 여부
  let reviewContent = ''; // 후기 내용
  let fileInput; // 파일 입력 (bind:this 사용)
  let isSubmitting = false; // 중복 요청 방지

  // 여행지 목록 가져오기
  async function fetchDestinations() {
    try {
      const response = await fetch("http://localhost:9000/pois");
      if (!response.ok) throw new Error("데이터를 불러오는 데 실패했습니다.");
      
      const data = await response.json();
      
      // POI_NM과 POI_IDX를 저장
      pois = data.map(item => ({ name: item.POI_NM, id: item.POI_IDX }));
      destinations = pois.map(item => item.name); // 자동완성용 여행지 목록 설정
    } catch (error) {
      console.error("여행지 데이터를 불러오지 못했습니다:", error);
    }
  }

  // 컴포넌트 마운트 시 API 호출
  onMount(fetchDestinations);

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

  let selectedPOI = null; // 선택한 POI 정보 저장

  function selectDestination(destination) {
    query = destination;
    results = [];
    isDropdownVisible = false;

    // POI_NM과 일치하는 POI_IDX 찾기
    selectedPOI = pois.find(poi => poi.name === destination);
  }

  $: filterDestinations();

  function getRandomDestinations() {
    let shuffled = [...destinations].sort(() => Math.random() - 0.3);
    return shuffled.slice(0, 3);
  }

  function handleFocus() {
    results = getRandomDestinations();
    isDropdownVisible = true;
  }

  let reviewImage = [];  // 기본값을 빈 배열로 설정

  // 파일 입력 필드 바인딩
function handleFileChange(event) {
  // 선택된 파일을 확인하는 부분
  console.log("선택된 파일:", event.target.files);
}

// ✅ 후기 제출 처리 (로그인한 사용자 ID 포함)
function handleSubmit(event) {
  if (isSubmitting) return; // 중복 제출 방지
  isSubmitting = true;

  if (!destinations.includes(query)) {
    alert('목록에 있는 여행지나 검색한 여행지를 선택해주세요.');
    event.preventDefault();
    isSubmitting = false;
    return;
  }

  if (!reviewContent.trim()) {
    alert('후기 내용을 작성해주세요.');
    event.preventDefault();
    isSubmitting = false;
    return;
  }

  if (fileInput.files.length === 0) {
    alert('후기 이미지를 업로드해주세요.');
    event.preventDefault();
    isSubmitting = false;
    return;
  }

  const POI_IDX = selectedPOI ? selectedPOI.id : null;
  const formData = new FormData();
  formData.append("POI_IDX", POI_IDX);
  formData.append("USER_ID", user);
  formData.append("REVIEW_CONTENT", reviewContent);
  formData.append("review_file", fileInput.files[0]);

  fetch("http://localhost:9000/reviews", {
    method: "POST",
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      alert("리뷰가 등록되었습니다!");
      console.log("등록 성공:", data);
      window.history.back();
    })
    .catch(error => {
      console.error("등록 실패:", error);
      alert("등록에 실패했습니다.");
    })
    .finally(() => {
      isSubmitting = false; // 요청이 끝난 후 다시 제출 가능하도록 설정
    });
}


  function goBack() {
    window.history.back();
  }

  
</script>

<style>
 /* .text-muted {
  display:none;
 } */

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
  <div class={`visual-zone visual_review`}>
    <p>여행을 다녀온 후기를 서로 공유해보세요</p>
    <h1>여행후기</h1>
  </div>

  <div class="content">
    <div class="d-flex justify-content-center align-items-center centered-container">
      <h5>여행후기 등록</h5>
    </div>
    
    <form on:submit|preventDefault={handleSubmit}>
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
              <li class="list-group-item autocomplete-item" on:click={() => selectDestination(result)}>
                {result}
              </li>
            {/each}
          </ul>
        {/if}
      </div>

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

      <div class="form-row">
        <label for="reviewImage" class="form-label required-label">후기 이미지</label>
        <input
          class="form-control"
          type="file"
          id="reviewImage"
          accept="image/*"
          bind:this={fileInput}
          required
        />
      </div>

      <div class="button-container">
        <button type="button" class="btn btn-cancel" on:click={goBack}>취소</button>
        <button type="submit" class="btn btn-submit">등록</button>
      </div>
    </form>
  </div>
</main>
