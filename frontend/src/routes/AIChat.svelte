<script>
  import { onMount, afterUpdate } from "svelte";
  import { initializeChat, sendMessage, scrollToBottom } from "../assets/js/AIChat.js";

  let messages = [];
  let startDate = "";
  let endDate = "";
  let companion = "";
  let region = "";
  let style = "";
  let schedule = "";
  let showConfirmButton = false;
  let showCalendar = false;
  let selectedData = {}; // ✅ 선택된 데이터를 저장할 객체 추가

  const API_URL = "http://localhost:9000/chat";

  onMount(() => {
    initializeChat((initialMessages) => {
      messages = initialMessages.map((msg, index) => ({
        id: `init-${index}`,
        ...msg,
      }));
      scrollToBottom();
    });
  });

  afterUpdate(() => {
    scrollToBottom();
  });

  function generateUniqueId() {
    return `${new Date().getTime()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  function updateMessages(newMessage) {
    messages = [...messages, { id: generateUniqueId(), ...newMessage }];
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

    const formattedStartDate = startDate.replace(/-/g, "/");
    const formattedEndDate = endDate.replace(/-/g, "/");

    const dateMessage = `📅 여행 일정: ${formattedStartDate} ~ ${formattedEndDate}`;
    showCalendar = false;

    selectedData["여행 일정"] = `${formattedStartDate} ~ ${formattedEndDate}`;

    updateMessages({ type: "user", text: dateMessage });

    updateMessages({
      id: generateUniqueId(),
      type: "bot",
      text: "(2/5) 이번 여행은 누구랑 함께 하실 예정이신가요?",
      buttons: [
        { text: "가족", action: "schedule_family" },
        { text: "연인", action: "schedule_couple" },
        { text: "친구", action: "schedule_friends" },
        { text: "혼자", action: "schedule_alone" },
      ],
    });
  }
</script>

<main>
  <div class="chat-container">
    <div class="chatbot-window" id="chatWindow">
      <div class="chat-header">
        <h3>챗봇 봄봄</h3>
      </div>
      <div class="chat-body">
        {#each messages as message, i}
          <div class="message-wrapper {message.type}">
            {#if message.type === "bot" && i === 0}
              <div class="bot-profile-wrapper">
                <div class="bot-profile">
                  <img src="/src/assets/img/chatbot_profile.png" alt="봄봄" class="bot-img" />
                  <span class="bot-name">여행AI 봄봄</span>
                </div>
              </div>
            {/if}
            <div class={message.type === "bot" ? "message-bot" : "message-user"}>
              {@html message.text}
            </div>

            {#if message.showCalendar}
              <div class="message-wrapper bot">
                <div class="message-bot">
                  <label for="start-date">🛫 여행 시작일:</label>
                  <input type="date" id="start-date" bind:value={startDate} on:change={(e) => handleDateChange(e, "start")} />
                  <label for="end-date">🏁 여행 종료일:</label>
                  <input type="date" id="end-date" bind:value={endDate} on:change={(e) => handleDateChange(e, "end")} />
                  {#if showConfirmButton}
                    <button class="confirm-btn" on:click={confirmDates}>확인</button>
                  {/if}
                </div>
              </div>
            {/if}

            {#if message.buttons}
              <div class="button-wrapper">
                {#each message.buttons as button}
                  <button class="chat-btn" on:click={() => handleButtonClick(button.text, button.action)}>
                    {button.text}
                  </button>
                {/each}
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>
  </div>
</main>

<style>
  /* 챗봇 컨테이너 */
  .chat-container {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
  }

  .chatbot-window {
    height: 75vh;
    overflow-y: auto;
    background-color: #ffecb9;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .chat-header {
    text-align: center;
    color: #000;
    padding: 10px;
    font-size: 18px;
    font-weight: bold;
    background-color: #f8d17d;
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
  }

  .message-bot {
    background-color: white;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 70%;
    word-wrap: break-word;
  }

  .message-user {
    background-color: #d1e7dd;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 70%;
    word-wrap: break-word;
  }

  .button-wrapper {
    display: flex;
    gap: 10px;
  }

  .chat-btn {
    background-color: white;
    color: black;
    border: 1px solid #ddd;
    padding: 10px 18px;
    border-radius: 20px;
    cursor: pointer;
  }

  .chat-btn:hover {
    background-color: #f1f1f1;
  }

  .confirm-btn {
    margin-top: 10px;
    padding: 10px;
    border: none;
    background-color: #f8d17d;
    border-radius: 20px;
  }
</style>
