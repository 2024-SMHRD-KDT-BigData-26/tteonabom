<script>
  import { onMount, afterUpdate } from "svelte";
  import {
    initializeChat,
    sendMessage,
    scrollToBottom,
    fetchDataFromAPI,
    downloadExcelFile, // 추가
    saveChatContent, // 추가
  } from "../assets/js/AIChat.js";

  let messages = [];
  let startDate = "";
  let endDate = "";
  let showConfirmButton = false;
  let showCalendar = false;
  let selectedData = {}; // ✅ 선택된 데이터를 저장할 객체 추가
  let currentCroomId = 192; // 기본값을 192로 설정 (임시 값으로 시작)

  onMount(() => {
    initializeChat((initialMessages) => {
      messages = initialMessages;
      scrollToBottom();
    });
  });

  afterUpdate(() => {
    scrollToBottom();
  });

  function updateMessages(newMessage) {
    messages = [...messages, newMessage];
  }

  function handleUserMessage(text) {
    try {
      const result = sendMessage(
        messages,
        text,
        (value) => {
          if (value) {
            showCalendar = true;
          }
        },
        updateMessages,
        selectedData,
      );

      if (result && Array.isArray(result.updatedMessages)) {
        messages = result.updatedMessages;

        currentCroomId = 192; // 항상 192로 설정
      } else {
        console.error(
          "sendMessage 함수에서 올바른 updatedMessages를 반환하지 않았습니다.",
        );
      }
    } catch (error) {
      console.error("handleUserMessage 오류:", error);
    }
  }

  function handleButtonClick(text) {
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

    const formattedStartDate = startDate.replace(/-/g, "/");
    const formattedEndDate = endDate.replace(/-/g, "/");

    const dateMessage = `📅 여행 일정: ${formattedStartDate} ~ ${formattedEndDate}`;
    showCalendar = false;

    // ✅ 사용자가 선택한 날짜를 selectedData["여행 일정"]에 저장
    selectedData["여행 일정"] = `${formattedStartDate} ~ ${formattedEndDate}`;

    updateMessages({ type: "user", text: dateMessage });

    updateMessages({
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
      <div class="chat-header"><h3>챗봇 봄봄</h3></div>
      <div class="chat-body">
        {#each messages as message, i}
          <div class="message-wrapper {message.type}">
            {#if message.type === "bot" && i === 0}
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
              class={message.type === "bot" ? "message-bot" : "message-user"}
            >
              {@html message.text}
            </div>
            {#if message.showCalendar}
              <div class="message-wrapper bot">
                <div class="message-bot">
                  <label for="start-date">🛫 여행 시작일:</label>
                  <input
                    type="date"
                    id="start-date"
                    bind:value={startDate}
                    on:change={(e) => handleDateChange(e, "start")}
                  />
                  <label for="end-date">🏁 여행 종료일:</label>
                  <input
                    type="date"
                    id="end-date"
                    bind:value={endDate}
                    on:change={(e) => handleDateChange(e, "end")}
                  />
                  {#if showConfirmButton}
                    <button class="confirm-btn" on:click={confirmDates}
                      >확인</button
                    >
                  {/if}
                </div>
              </div>
            {/if}
            {#if message.buttons}
              <div class="button-wrapper">
                {#each message.buttons as button, index}
                  <button
                    class="chat-btn"
                    on:click={() => {
                      if (!button.disabled) {
                        handleButtonClick(button.text);
                        message.buttons[index].disabled = true; // 클릭 후 버튼 비활성화

                        if (button.text === "일정 다운로드") {
                          const chatId = 91; // 임의 값 (또는 실제 chatId 사용)
                          downloadExcelFile(chatId); // 엑셀 다운로드 함수 호출
                        } else if (button.text === "채팅 내용 저장") {
                          const userId = "kakao_3910835997"; // 로그인된 사용자 ID로 변경
                          const croomId = 313; // 임의 croomId 설정 (또는 실제 croomId 사용)
                          saveChatContent(croomId, userId); // 저장 함수 호출
                        }
                      }
                    }
                  }
                  >
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
    /* 내용 제목 스타일 강제 적용 */
    :global(.message-user h1) {
  font-size: 22px !important;
}

  /* 내용 제목 스타일 강제 적용 */
  :global(.message-user h2) {
  font-size: 20px !important;
}

  /* 내용 제목 스타일 강제 적용 */
  :global(.message-user h3) {
  font-size: 20px !important;
}

  /* 챗봇 영역 */
  .chat-container {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
  }
  /* 챗봇 창 */
  .chatbot-window {
    height: 75vh;
    overflow-y: auto;
    background-color: #ffecb9;
    padding: 15px;
    border-radius: 10px;
  }
  /* header */
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
    background-color: white;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 50%;
    font-size: 14px;
    margin-bottom: 10px;
  }

  .message-user {
    background-color: #d1e7dd;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 50%;
    font-size: 14px;
    text-align: right;
    min-height: 0px;
    display: none;
  }
  .message-user:not(:empty) {
    display: block; /* 내용이 있을 때만 표시 */
  }

  .button-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: left;
    gap: 10px;
  }

  .button-wrapper button,
  .confirm-btn {
    font-family: "Paperlogy-6SemiBold";
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
  /* 캘린더 */
  .calendar-message {
    max-width: 80%;
    word-wrap: break-word;
    text-align: center;
  }

  .confirm-btn {
    margin-top: 10px;
    transform: translate(90px, 0%);
    color: #333;
    background-color: #ffdaab;
  }

  .confirm-btn:hover {
    background-color: #ffd59f;
  }

  .message-bot input[type="date"] {
    width: 100%;
    padding: 5px;
    margin-top: 5px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
</style>
