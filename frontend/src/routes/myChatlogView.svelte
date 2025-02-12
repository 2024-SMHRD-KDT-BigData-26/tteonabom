<script>
  import { onMount } from "svelte";

let messages = [];
let croomId = 0;
// ✅ 백엔드에서 대화 내역을 가져오는 함수
async function fetchChatMessages(croomId) {
    if (isNaN(croomId) || croomId <= 0) {
      console.error("🚨 올바르지 않은 CROOM_IDX:", croomId);
      return;
    }

    try {
      const response = await fetch(`http://localhost:9000/chat/croom/${croomId}`);
      console.log("✅ API 응답 상태 코드:", response.status);

      // ✅ JSON 응답인지 확인
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        throw new Error("❌ API가 JSON 응답이 아님 (HTML 응답일 가능성 있음)");
      }

      const data = await response.json();
      console.log("✅ API 응답 데이터:", data);

      // ✅ 응답이 배열인지 확인
      if (!Array.isArray(data)) {
        console.error("🚨 API 응답이 배열이 아님:", data);
        return;
      }

      messages = data.map(chat => ({
        type: chat.user_id === "봄봄" ? "bot" : "user",
        text: chat.message
      }));
    } catch (error) {
      console.error("❌ Error loading chat messages:", error);
    }
  }

  // ✅ 페이지가 로드될 때 CROOM_IDX 가져오기
  onMount(() => {
  const hashParts = window.location.hash.split("/").filter(Boolean); // 빈 요소 제거
  console.log("📌 URL 해시 경로:", hashParts); // 디버깅 로그

  if (hashParts.length > 1 && /^\d+$/.test(hashParts[hashParts.length - 1])) {
    croomId = parseInt(hashParts[hashParts.length - 1], 10);
    console.log("✅ 변환된 CROOM_IDX:", croomId);
    fetchChatMessages(croomId);
  } else {
    console.error("🚨 CROOM_IDX를 찾을 수 없거나 올바르지 않습니다.", hashParts);
  }
});

// ✅ 상세 페이지 이동
function goToDetail(id) {
  window.location.href = `#/${id}`;
}
</script>

<main class="main-content">
  <div class="content">
    <div class="container">
      <!-- 왼쪽 메뉴 -->
      <div class="list-group">
        <div class="list-group-item active" on:click={() => goToDetail("My")}>
          내 채팅로그
        </div>
        <div class="list-group-item" on:click={() => goToDetail("MyReview")}>
          내 여행후기
        </div>
        <div class="list-group-item" on:click={() => goToDetail("MyInfo")}>
          내 정보변경
        </div>
      </div>

      <!-- 오른쪽 콘텐츠 -->
      <div class="my-content">
        <div class="chatbot-window" id="chatWindow">
          <div class="chat-header"><h3>챗봇 봄봄</h3></div>
          <div class="chat-body">
            {#each messages as message}
              <div class="message-wrapper {message.type}">
                {#if message.type === "bot"}
                  <div class="bot-profile-wrapper">
                    <div class="bot-profile">
                      <img
                        src="/src/assets/img/chatbot_profile.png"
                        alt="봄봄"
                        class="bot-img"
                      />
                      <span class="bot-name">여행AI 봄봄</span>
                    </div>
                  </div>
                {/if}
                <div
                  class={message.type === "bot"
                    ? "message-bot"
                    : "message-user"}
                >
                {@html message.text
                  .replace(/```html/g, "")  // 백틱 블록 제거
                  .replace(/```/g, "")      // 남은 백틱 제거
                  .replace(/<br>/g, "")}    // 불필요한 <br> 제거
                </div>
              </div>
            {/each}
          </div>
        </div>
        <!-- 목록 버튼 -->
        <div class="btn-container-back">
          <button
            class="btn btn-secondary"
            on:click={() => window.history.back()}>목록</button
          >
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  .container {
    display: flex;
  }

  /* 왼쪽 메뉴 전체 */
  .list-group {
    margin-top: 25px;
  }

  /* 왼쪽 메뉴 아이템 */
  .list-group-item {
    cursor: pointer;
    width: 200px;
  }

  .list-group-item.active {
    background-color: #333;
    border-color: #333;
  }

  /* 오른쪽 콘텐츠 */
  .my-content {
    flex: 1;
    margin-left: 25px;
    margin-top: 5px;
  }

  .chatbot-window {
    height: 586px;
    overflow-y: auto;
    background-color: #ffecb9;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-height: 80vh;
  }

  .chat-header {
    text-align: center;
    color: #000;
    padding: 10px;
    border-radius: 10px 10px 0 0;
  }

  .message-wrapper {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
  }

  .message-wrapper.bot {
    align-items: flex-start;
  }

  .message-wrapper.user {
    align-items: flex-end;
  }

  .bot-profile-wrapper {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    margin-left: 10px;
  }

  .bot-profile {
    display: flex;
    align-items: center;
  }

  .bot-img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }

  .bot-name {
    font-size: 14px;
    font-weight: bold;
    font-family: "Paperlogy-6SemiBold";
  }

  .message-bot {
    background-color: #f8f9fa;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 50%;
    margin-left: 10px;
    font-size: 14px;
  }

  .message-user {
    background-color: #d1e7dd;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 50%;
    font-size: 14px;
    text-align: right;
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
