<script>
  import { onMount } from "svelte";
  import { initializeChat, sendMessage, scrollToBottom } from "../assets/js/AIChat.js";

  let messages = [];
  let showCalendar = false;
  let startDate = "";
  let endDate = "";
  let showConfirmButton = false;

  onMount(() => {
    initializeChat((initialMessages) => {
      messages = initialMessages;
      scrollToBottom();
    });
  });

  function updateMessages(newMessage) {
    messages = [...messages, newMessage];
    scrollToBottom();
  }

  function handleUserMessage(text) {
    const { updatedMessages } = sendMessage(messages, text, (value) => {
      showCalendar = value;
    });

    messages = updatedMessages;
  }

  function handleButtonClick(text) {
    // 사용자 메시지 중복 방지를 위해 updateMessages() 호출 제거
    handleUserMessage(text);
  }

  function handleDateChange(event, type) {
    if (type === "start") {
      startDate = event.target.value;
      endDate = "";
    } else if (type === "end") {
      if (!startDate) {
        alert("먼저 여행 시작일을 선택해주세요.");
        return;
      }
      if (event.target.value < startDate) {
        alert("종료일은 시작일보다 이후여야 합니다.");
        return;
      }
      endDate = event.target.value;
    }
    checkConfirmButton();
  }

  function checkConfirmButton() {
    showConfirmButton = startDate !== "" && endDate !== "";
  }

  function confirmDates() {
    if (!startDate || !endDate) return;

    const dateMessage = `📅 여행 일정: ${startDate} ~ ${endDate}`;

    // 중복 방지를 위해 사용자 메시지만 추가
    updateMessages({ type: "user", text: dateMessage });

    // 챗봇 메시지에도 날짜 표시 후 다음 질문으로 진행
    updateMessages({
      type: "bot",
      text: "(2/5) 이번 여행은 누구랑 함께 하실 예정이신가요?",
      buttons: [
        { text: "가족", action: "family" },
        { text: "연인", action: "couple" },
        { text: "친구", action: "friends" },
        { text: "혼자", action: "alone" },
      ],
    });

    showCalendar = false;
    showConfirmButton = false;
  }
</script>

<main class="chat-container">
  <div class="chatbot-window" id="chatWindow">
    <div class="chat-header"><h3>챗봇 봄봄</h3></div>
    <div class="chat-body">
      {#each messages as message}
        <div class="message-wrapper {message.type}">
          {#if message.type === "bot"}
            <div class="bot-profile-wrapper">
              <div class="bot-profile">
                <img src="/src/assets/img/chatbot_profile.png" alt="봄봄" class="bot-img" />
                <span class="bot-name">여행AI 봄봄</span>
              </div>
            </div>
          {/if}
          <div class="{message.type === "bot" ? "message-bot" : "message-user"}">
            {@html message.text}
          </div>
          {#if message.buttons}
            <div class="button-wrapper">
              {#each message.buttons as button}
                <button class="chat-btn" on:click={() => handleButtonClick(button.text)}>
                  {button.text}
                </button>
              {/each}
            </div>
          {/if}
        </div>
      {/each}

      {#if showCalendar}
        <div class="calendar-container">
          <label for="start-date">🛫 여행 시작일:</label>
          <input type="date" id="start-date" bind:value={startDate} on:change={(e) => handleDateChange(e, "start")} />

          <label for="end-date">🏁 여행 종료일:</label>
          <input type="date" id="end-date" bind:value={endDate} on:change={(e) => handleDateChange(e, "end")} />

          {#if showConfirmButton}
            <button class="confirm-btn" on:click={confirmDates}>✅ 확인</button>
          {/if}
        </div>
      {/if}
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

  .chat-container {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
  }

  .chatbot-window {
    height: 80vh;
    overflow-y: auto;
    background-color: #ffecb9;
    padding: 15px;
    border-radius: 10px;
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
    font-family: 'Paperlogy-6SemiBold';
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

  .button-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: left;
    gap: 10px;
    margin: 10px 0 20px 10px;
  }

  .button-wrapper button {
    font-family: 'Paperlogy-6SemiBold';
    font-size: 14px;
    padding: 10px 18px;
    border-radius: 20px;
    background-color: white;
    color: black;
    border: none;
    cursor: pointer;
  }

  .button-wrapper button:hover {
    background-color: #f1f1f1;
  }
</style>
