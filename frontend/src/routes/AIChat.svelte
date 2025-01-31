<script>
  let prompt = '';  // 사용자 입력을 받을 변수
  let response = ''; // 챗봇 응답을 받을 변수
  let loading = false; // 요청 중임을 알리는 변수

  // 여행지 추천 요청 함수
  async function fetchDestination() {
    loading = true; // 요청 중 표시
    try {
      const res = await fetch('http://127.0.0.1:9000/recommend_destination', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt })  // 사용자 입력 prompt를 서버로 전송
      });
      
      const data = await res.json();
      if (data.answer) {
        response = data.answer;  // 서버로부터 받은 응답
      } else {
        response = 'No answer received from the server.';
      }
    } catch (error) {
      console.error('Error:', error);
      response = 'Error occurred while fetching data. Please try again later.';
    } finally {
      loading = false; // 요청 완료 후 상태 변경
    }
  }

  // 여행 일정 추천 요청 함수
  async function fetchItinerary() {
    loading = true; // 요청 중 표시
    try {
      const res = await fetch('http://127.0.0.1:9000/recommend_itinerary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt })  // 사용자 입력 prompt를 서버로 전송
      });

      const data = await res.json();
      if (data.answer) {
        response = data.answer;  // 서버로부터 받은 응답
      } else {
        response = 'No answer received from the server.';
      }
    } catch (error) {
      console.error('Error:', error);
      response = 'Error occurred while fetching data. Please try again later.';
    } finally {
      loading = false; // 요청 완료 후 상태 변경
    }
  }
</script>

<main>
  <h1>여행 AI 챗봇</h1>

  <label for="prompt">여행 관련 질문 입력:</label>
  <input id="prompt" type="text" bind:value={prompt} placeholder="예시: 서울 여행지 추천 해줘" />

  <button on:click={fetchDestination} disabled={loading}>여행지 추천</button>
  <button on:click={fetchItinerary} disabled={loading}>여행 일정 추천</button>

  {#if loading}
    <p>로딩 중...</p> <!-- 요청 중일 때 로딩 표시 -->
  {/if}

  {#if response}
    <div>
      <h3>결과:</h3>
      <p>{response}</p>
    </div>
  {/if}
</main>

<style>
  main {
    padding: 2em;
    text-align: center;
  }

  input, button {
    padding: 0.5em;
    margin: 0.5em;
  }

  button {
    cursor: pointer;
  }

  button:disabled {
    background-color: #ddd;
    cursor: not-allowed;
  }
</style>
