<script>
  // 비주얼존 배경명
  let currentPage = 'visual_review';

  // 네비바 CSS
  import '../assets/css/VisualZone.css';

  // 후기 목록
  import { recentReviews } from '../assets/js/recent-review-data.js';

  // 시간 변환
  import { timeAgo } from "../assets/js/timeAgo.js";

  // 첫 번째 후기 불러오기(예시)
  let review = recentReviews[0];

  ////////// 이미지 확대 모달 관련
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

  // 리뷰 삭제
  function deleteReview(reviewIdx) {
    console.log(`Review with ID ${reviewIdx} has been deleted.`);
    showModal = false;
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
    margin-top: 20px;;
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
  }

  .review-info strong {
    font-size: 18px;
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

  /* 수정, 삭제 버튼을 최하단 오른쪽에 위치시키기 */
  .review-info .btn-container {
    position: absolute;
    bottom: 20px;
    right: 20px;
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
    <div class="review-detail d-flex">
      <div class="review-image">
        <img src={review.FILE_NM} alt="review image" class="img-fluid" on:click={toggleModal} style="cursor: pointer;" />
      </div>

      <!-- 이미지 확대 모달 -->
      {#if isModalOpen}
        <div class="modal" on:click={toggleModal}>
          <img src={review.FILE_NM} alt="여행지 이미지 (원본 크기)" />
        </div>
      {/if}

      <div class="review-info ms-3">
        <div class="d-flex align-items-center">
          <img src={review.USER_PROFILE_IMG} alt="user profile" class="rounded-circle" width="40" height="40" />
          <div class="ms-2">
            <strong>{review.USER_NICK}</strong>
            <div class="text-muted">{timeAgo(review.CREATED_AT)}</div>
          </div>
        </div>

        <div class="mt-3">
          <!-- 실제로는 여행지 번호와 매칭된 여행지 이름이 나와야 함-->
          <p><strong>{review.POI_IDX}</strong></p>
          <p>{review.REVIEW_CONTENT}</p>
        </div>

        <!-- 수정, 삭제 버튼 -->
        <div class="btn-container">
          <a href={`/#/reviewUpdate/`} class="btn update-btn">수정</a>
          <button class="btn delete-btn" on:click={() => openDeleteModal(review.REVIEW_IDX)}>삭제</button>
        </div>
      </div>
    </div>

    <!-- 목록 버튼 -->
    <div class="btn-container-back">
      <button class="btn btn-secondary" on:click={() => window.history.back()}>목록</button>
    </div>
  </div>

  <!-- 삭제 모달 -->
  {#if showModal}
    <!-- 삭제 모달 배경 -->
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
