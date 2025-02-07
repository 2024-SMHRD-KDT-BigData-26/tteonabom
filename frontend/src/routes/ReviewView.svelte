<script>
  // 페이지 이동을 위한 import
  import { link } from "svelte-spa-router";

  // 비주얼존 배경명
  let currentPage = 'visual_review';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  // 시간 변환
  import { timeAgo } from "../assets/js/timeAgo.js";


  // 리뷰 인덱스 받아오기
  export let params; 
  
  let review = {}; // 후기 데이터
  let user = ''; // 로그인 상태

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

    // params.REVIEW_IDX로 리뷰 데이터 불러오기
    const reviewIdx = params.REVIEW_IDX; // REVIEW_IDX를 params에서 가져옴
    fetchReview(reviewIdx); // 해당 REVIEW_IDX로 후기 데이터 불러오기
  });

  // 후기 목록을 API에서 받아오기
  async function fetchReview(reviewIdx) {
    try {
      const response = await fetch(`http://localhost:9000/reviews/${reviewIdx}`);
      if (response.ok) {
        review = await response.json(); // API에서 받은 JSON 데이터를 review 변수에 저장
      } else {
        console.error("Failed to load review data.");
      }
    } catch (error) {
      console.error("Error fetching review data:", error);
    }
  }

  ///////// 이미지 확대 모달 관련
  import { onMount } from 'svelte';
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

  ///////// 후기 삭제 모달 관련
  let showModal = false; // 삭제 모달 상태
  let currentReviewIdx = null; // 삭제할 리뷰의 인덱스

  // 모달 열기
  function openDeleteModal(reviewIdx) {
    showModal = true;
    currentReviewIdx = reviewIdx;
  }

  // 리뷰 삭제 (서버 API 호출)
  async function deleteReview(reviewIdx) {
    try {
      const response = await fetch(`http://localhost:9000/reviews/${reviewIdx}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        // 삭제 후 UI에서 해당 리뷰를 제거하는 로직
        showModal = false;
        alert("리뷰가 성공적으로 삭제되었습니다.");
        // 필요한 경우 리뷰 목록을 새로 불러오거나 페이지를 리프레시할 수 있습니다.
        window.history.back(); // 삭제 후 이전 페이지로 돌아가기
      } else {
        alert("리뷰 삭제 실패");
      }
    } catch (error) {
      console.error("Error deleting review:", error);
      alert("리뷰 삭제 중 오류가 발생했습니다.");
    }
  }

  // 모달 배경 제거
  function closeModal() {
    showModal = false;
  }
</script>

<style>
  /* 후기 영역 */
  .review-detail {
    display: flex;
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 0.375rem;
    position: relative;
  }

  /* 후기 이미지 */
  .review-image img {
    width: 300px;
    height: auto;
    object-fit: cover;
    border-radius: 5px;
  }

  .review-info {
    flex: 1;
    margin-bottom: 25px;
  }

  /* 여행지 명 */
  .review-title {
    font-size: 24px;
    margin-bottom: 5px;
  }

  .review-info .text-muted {
    font-size: 14px;
  }

  /* 이미지 확대 모달 스타일 */
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
    z-index: 1050; /* 기존 모달보다 위에 표시 */
  }

  /* 모달 내 이미지 */
  .modal img {
    max-width: 90%;
    max-height: 90%;
    border-radius: 8px;
  }

  /* 후기 상세 컨텐츠 */
  .content {
    position: relative;
  }

/* 수정, 삭제 버튼을 후기 아래로 위치시키기 */
.review-info .btn-container {
  position: absolute; /* 버튼을 고정시킴 */
  bottom: 20px; /* 하단 20px */
  right: 20px; /* 오른쪽 20px */
  display: flex;
  gap: 20px; /* 버튼 간격 */
}

  /* 삭제 모달 배경*/
  .modal-delete-backdrop.show {
    background-color: rgba(0, 0, 0, 0.8); 
    z-index: 1040 !important; /* 모달 백그라운드가 모달 내용보다 아래로 나오도록 */
  }

  /* 삭제 모달 */
  .modal-content {
    padding: 20px;
    border-radius: 8px;
    position: relative;
    z-index: 1050; /* 모달 내용이 백그라운드 위에 오도록 설정 */
  }

  .modal-header, .modal-footer {
    border: none;
  }

  .modal-footer button {
    width: 100px;
  }

  /* 삭제 모달 중앙 배치 */
  .modal-dialog {
    max-width: 500px; /* 최대 너비 */
    margin: 30vh auto; /* 화면의 상단에서 30% 떨어진 위치로 중앙 정렬 */
  }

  /* 삭제 모달을 보이게 하는 스타일 */
  .modal.fade.show {
    display: block;
  }

  /* 버튼 스타일 */
  .btn {
    padding: 10px 20px;
    font-size: 14px;
  }

  /* 수정 버튼 */
  .update-btn, .close-btn {
    padding: 5px 20px;
    background-color: #ABB5BE;
    color: #fff;
  }

  .update-btn:active {
    background-color: #ABB5BE;
    color: #fff;
  }

  /* 삭제 버튼 */
  .delete-btn {
    padding: 5px 20px;
    background-color: #FF5D17;
    color: #fff;
  }

  .delete-btn:active {
    background-color: #FF5D17;
    color: #fff;
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
    <p>여행을 다녀온 후기를 서로 공유해보세요</p>
    <h1>여행후기</h1>
  </div>

  <!-- 여행후기 상세 컨텐츠 영역 -->
  <div class="content">
    <!-- 첫 번째 리뷰 상세 내용 -->
    {#if review.REVIEW_IDX} <!-- 로딩되었을 때만 렌더링 -->
    <div class="review-detail d-flex">
      <div class="review-image">
        <img src={`http://localhost:9000/images/${review.FILE_URL}`} alt="review image" class="img-fluid" on:click={toggleModal} style="cursor: pointer;" />
      </div>

      <!-- 이미지 확대 모달 -->
      {#if isModalOpen}
        <div class="modal" on:click={toggleModal}>
          <img src={`http://localhost:9000/images/${review.FILE_URL}`} alt="여행지 이미지 (원본 크기)" />
        </div>
      {/if}

      <div class="review-info ms-3">
        <div class="d-flex align-items-center">
          <img src={`http://localhost:9000/images/${review.USER_PROFILE_IMG}`} 
            alt="프로필 이미지" 
            class="rounded-circle"
            width="40" height="40"
            on:load={() => {
              if (masonryInstance) {
                masonryInstance.reloadItems();
                masonryInstance.layout();
              }
            }}
            on:error={(event) => {
              event.target.src = '../src/assets/img/default_profile_image.png';  // 디폴트 이미지 경로
            }}
            />
          <div class="ms-2">
            <strong>{review.USER_NICK}</strong>
            <div class="text-muted">{timeAgo(review.CREATED_AT)}</div>
          </div>
        </div>

        <div class="mt-3">
          <p class="review-title"><strong>{review.POI_NM}</strong></p>
          <p>{@html review.REVIEW_CONTENT.replace(/\n/g, '<br />')}</p>
        </div>

        <!-- 수정, 삭제 버튼을 로그인한 사용자와 비교하여 표시 -->
        {#if user === review.USER_ID}
          <div class="btn-container">
            <a use:link href="/ReviewUpdate/{review.REVIEW_IDX}" class="btn update-btn">수정</a>
            <button class="btn delete-btn" on:click={() => openDeleteModal(review.REVIEW_IDX)}>삭제</button>
          </div>
        {/if}
      </div>
    </div>
    {/if}

    <!-- 목록 버튼 -->
    <div class="btn-container-back">
      <button class="btn btn-secondary" on:click={() => window.history.back()}>목록</button>
    </div>
  </div>

  <!-- 삭제 모달 -->
  {#if showModal}
    <div class="modal-delete-backdrop show" on:click={closeModal}></div>
    <div class="modal fade show" tabindex="-1" style="display: block;" aria-modal="true" role="dialog">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">여행후기 삭제</h5>
            <button type="button" class="btn-close" on:click={closeModal}></button>
          </div>
          <div class="modal-body">
            <p>여행후기를 삭제하시겠습니까?
              <br>
              삭제한 후기는 복구할 수 없습니다!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary close-btn" on:click={closeModal}>취소</button>
            <button type="button" class="btn delete-btn" on:click={() => deleteReview(currentReviewIdx)}>삭제</button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</main>
