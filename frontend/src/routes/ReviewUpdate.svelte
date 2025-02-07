<script>
  import { onMount } from "svelte";

  // 로그인 상태 관리
  let user = '';

  // 리뷰 인덱스 받아오기
  export let params;
  let reviewIdx = params.REVIEW_IDX;

  let review = {}; // 후기 데이터
  let query = ''; // 여행지 선택 (자동완성)
  let reviewContent = ''; // 후기 내용
  let reviewImage = review.FILE_URL || ''; // 이미지 URL 저장
  let fileInput; // 파일 입력 (bind:this 사용)

  // 여행지 자동완성 기능
  let destinations = []; // 여행지 목록
  let pois = []; // POI 데이터 저장
  let results = []; // 자동완성 목록
  let isDropdownVisible = false; // 자동완성 목록 표시 여부
  let selectedPOI = null; // 선택한 POI 정보 저장

  // API에서 후기 데이터 불러오기
async function fetchReview(reviewIdx) {
  try {
    const response = await fetch(`http://localhost:9000/reviews/${reviewIdx}`);
    if (response.ok) {
      review = await response.json();
      query = review.POI_NM || ''; // 여행지 자동 입력
      reviewContent = review.REVIEW_CONTENT || ''; // 후기 내용 자동 입력
      reviewImage = review.FILE_URL ? `http://localhost:9000/images/${review.FILE_URL}` : ''; // 이미지 URL 설정
      selectedPOI = { name: review.POI_NM, id: review.POI_IDX }; // 선택한 POI 정보 설정
    } else {
      console.error("Failed to load review data.");
    }
  } catch (error) {
    console.error("Error fetching review data:", error);
  }
}


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
  onMount(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        user = JSON.parse(storedUser).USER_ID || '';
      } catch (error) {
        console.error("로그인 정보 파싱 오류:", error);
        user = '';
      }
    }
    fetchReview(reviewIdx);
    fetchDestinations();
  });

  // 이미지 변경 핸들러
  function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    reviewImage = URL.createObjectURL(file); // 새로운 이미지 미리보기
  }
}

  // 여행지 필터링
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

  // 여행지 선택
  function selectDestination(destination) {
    query = destination;
    results = [];
    isDropdownVisible = false;

    // POI_NM과 일치하는 POI_IDX 찾기
    selectedPOI = pois.find(poi => poi.name === destination);
  }

  // 랜덤 여행지 추천
  function getRandomDestinations() {
    let shuffled = [...destinations].sort(() => Math.random() - 0.3);
    return shuffled.slice(0, 3);
  }

  // 입력 필드 포커스 시 랜덤 여행지 표시
  function handleFocus() {
    results = getRandomDestinations();
    isDropdownVisible = true;
  }

  // 수정 제출 처리
  async function handleSubmit(event) {
  event.preventDefault();

  if (!query.trim() || !reviewContent.trim()) {
    alert("여행지와 후기를 모두 입력해주세요.");
    return;
  }

  const formData = new FormData();
  formData.append("review_content", reviewContent);
  formData.append("poi_nm", query);
  
  if (selectedPOI) {
    formData.append("poi_idx", selectedPOI.id);
  } else {
    formData.append("poi_idx", ""); // POI_IDX가 없으면 빈 값으로 전송
  }

  if (fileInput.files.length > 0) {
    formData.append("review_file", fileInput.files[0]);
  }

  console.log("전송할 폼 데이터:", {
    review_content: reviewContent,
    poi_nm: query,
    poi_idx: selectedPOI ? selectedPOI.id : "없음",
    review_file: fileInput.files.length > 0 ? fileInput.files[0].name : "",
  });

  try {
    const response = await fetch(`http://localhost:9000/reviews/${reviewIdx}`, {
      method: "PUT",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("수정에 실패했습니다.");
    }

    const data = await response.json();
    alert("리뷰가 수정되었습니다!");
    console.log("✅ 수정 성공:", data);
    window.history.back();
  } catch (error) {
    console.error("❌ 수정 실패:", error);
    alert("수정에 실패했습니다.");
  }
}

  // 뒤로가기
  function goBack() {
    window.history.back();
  }

  // 자동완성 필터링을 위한 반응형 처리
  $: filterDestinations();
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
  
  /* 기존 이미지 라벨 */
  .image-label {
    padding-left: 12px;
  }
</style>

<main class="main-content">
  <div class="content">
    <h5>여행후기 수정</h5>
    
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
          required
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
        <textarea class="form-control" id="reviewContent" rows="8" bind:value={reviewContent} required></textarea>
      </div>

      <div class="form-row">
        <label for="reviewImage" class="form-label required-label">후기 이미지</label>
        <input type="file" class="form-control" id="reviewImage" accept="image/*" bind:this={fileInput} on:change={handleFileChange} />
      </div>

      {#if reviewImage}
      <div class="form-row">
        <label class="form-label image-label">이미지 확인</label>
        <div class="image-preview">
          <img src={reviewImage} alt="미리보기 이미지" width="100" height="100" />
        </div>
      </div>
      {/if}

      <div class="button-container">
        <button type="button" class="btn btn-cancel" on:click={goBack}>취소</button>
        <button type="submit" class="btn btn-submit">수정</button>
      </div>
    </form>
  </div>
</main>