<script>
  // 비주얼존 배경명
  let currentPage = 'visual_AI';

  // 비주얼존 CSS
  import '../assets/css/VisualZone.css';
</script>

<main class="main-content">
  <!-- 비주얼 존 -->
  <div class={`visual-zone ${currentPage}`}>
    <p>나에게 꼭 맞는 여행정보를 알려드려요</p>
    <h1>여행AI</h1>
  </div>

  <!-- 여행AI 채팅 컨텐츠 영역 -->
  <div class="content">
    <div style="width: 1078px; height: 1465px; background-color:#eee">
      
      <!-- 챗봇 대화창 -->
      <div class="container my-4">
        <div class="card chatbot-window" id="chatwindow">
          <div class="chat-header">
            <h3>챗봇 떠나봄</h3>
          </div>
          <div class="card-body" id="chatWindow">
            <!-- 초기 메시지 -->
            <div class="message-bot">
              안녕하세요!
              여행의 시작부터 끝까지
              떠나봄의 여행AI 봄봄입니다!

              AI가 당신의 완벽한 여행을 도와드립니다!

              아래에서 원하는 추천 버튼을 클릭해주세요.
            </div>

            <!-- 버튼 선택지 -->
            <div class="btns d-flex flex-wrap gap-2" id="buttonoptions">
              <button class="btn" id="datePickerButton">여행 일정 추천</button>
              <button class="btn">여행지 추천</button>
              <button class="btn">테마별 쇼핑몰 추천</button>
            </div>
          </div>
        </div>

        <!-- 날짜 입력 -->
        <div class="form-group mt-4" id="datePickerContainer" style="display: none;">
          <label for="dateInput" class="form-label">날짜를 선택하세요:</label>
          <input type="text" class="form-control" id="dateInput" placeholder="YYYY-MM-DD">
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  @font-face {
    font-family: 'Paperlogy-4Regular';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-4Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
  }

  @font-face {
    font-family: 'Paperlogy-6SemiBold';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-6SemiBold.woff2') format('woff2');
    font-weight: 600;
    font-style: normal;
  }

  * {
    font-family: 'Paperlogy-4Regular';
  }

  .chatbot-window {
    height: 80vh;
    overflow-y: auto;
    background-color: #FFECB9;
  }

  .chat-header h3 {
    color: white;
    font-family: 'Paperlogy-6SemiBold';
    margin: 10px;
    text-align: center;
  }

  .message-wrapper {
    display: flex;
    margin-bottom: 10px;
  }

  .message-wrapper.bot {
    justify-content: flex-start;
  }

  .message-bot {
    background-color: #F8F9FA;
    color: #000;
    padding: 10px 15px;
    border-radius: 10px;
    max-width: 60%;
    text-align: left;
  }

  .message-wrapper.user {
    justify-content: flex-end;
  }

  .message-user {
    background-color: #D1E7DD;
    color: #000;
    padding: 10px 15px;
    border-radius: 10px;
    max-width: 60%;
    text-align: right;
  }

  .btns {
    margin-top: 20px;
    justify-content: left;
  }

  .btn {
    font-family: 'Paperlogy-6SemiBold';
    padding: 10px 20px;
    border-radius: 20px;
    font-size: 1rem;
    background-color: #FFFFFF;
    color: #000;
    box-shadow: gray;
  }

  .btn:hover {
    background-color: #FFA76A;
  }
</style>
