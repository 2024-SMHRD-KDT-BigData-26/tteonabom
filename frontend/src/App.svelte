<script>
  let data = null;
  let isLoading = true;
  let error = null;

  // 백엔드 API 호출
  async function getData() {
    try {
      const response = await fetch('http://localhost:9000/api/data');  // 백엔드 URL
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      data = await response.json();  // 백엔드에서 받아온 JSON 데이터
    } catch (e) {
      error = e.message;  // 오류가 있으면 오류 메시지 표시
    } finally {
      isLoading = false;  // 로딩 완료
    }
  }

  // API 호출
  getData();
</script>

<main>
  <h1>Data from Backend</h1>
  {#if isLoading}
    <p>Loading...</p>
  {:else if error}
    <p>Error: {error}</p>
  {:else}
    <pre>{JSON.stringify(data, null, 2)}</pre>  <!-- JSON 데이터 출력 -->
  {/if}
</main>

<style>
  h1 {
    color: #333;
    font-size: 2em;
  }

  pre {
    background-color: #f4f4f4;
    padding: 1em;
    border-radius: 8px;
    white-space: pre-wrap;  /* 긴 줄을 자동으로 감싸도록 설정 */
    word-wrap: break-word;  /* 긴 단어를 자동으로 줄 바꿈 */
    font-family: monospace; /* 가독성을 위한 고정폭 글꼴 사용 */
    max-width: 100%;  /* 화면을 넘어가지 않도록 설정 */
    overflow-x: auto;  /* 내용이 넘칠 경우 가로스크롤 */
  }
</style>
