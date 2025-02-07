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

  // 백엔드 API URL 설정
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


  function handleUserMessage(text) {
    const { updatedMessages } = sendMessage(
      messages,
      text,
      (value) => {
        if (value) {
          showCalendar = true;
        }
      },
      updateMessages,
      selectedData,
    ); // ✅ selectedData 전달
    messages = updatedMessages;

  }

  function handleButtonClick(text, field) {
    if (field === "recommendSchedule") {
      updateMessages({
        id: generateUniqueId(),
        type: "bot",
        text: "(1/5) 언제부터 언제까지 여행하실 계획인가요?",
        showCalendar: true,
      });
      return;
    }

    if (field === "companion") companion = text;
    else if (field === "region") region = text;
    else if (field === "style") style = text;
    else if (field === "schedule") schedule = text;

    updateMessages({ type: "user", text });

    if (field === "schedule") {
      sendToBackend();
    } else {
      const nextQuestion = getNextQuestion(field);
      updateMessages(nextQuestion);
    }
  }

  function getNextQuestion(field) {
    switch (field) {
      case "companion":
        return {
          id: generateUniqueId(),
          type: "bot",
          text: "(3/5) 여행하고 싶은 지역을 선택해주세요.",
          buttons: [
            { text: "수도권", action: "region" },
            { text: "서부권", action: "region" },
            { text: "동부권", action: "region" },
            { text: "제주권", action: "region" },
          ],
        };
      case "region":
        return {
          id: generateUniqueId(),
          type: "bot",
          text: "(4/5) 선호하는 여행 스타일을 선택해주세요.",
          buttons: [
            { text: "액티비티/체험", action: "style" },
            { text: "힐링/관광", action: "style" },
            { text: "핫플레이스", action: "style" },
          ],
        };
      case "style":
        return {
          id: generateUniqueId(),
          type: "bot",
          text: "(5/5) 일정 스타일을 선택해주세요.",
          buttons: [
            { text: "타이트한 일정", action: "schedule" },
            { text: "여유로운 일정", action: "schedule" },
          ],
        };
    }
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

    // 🛠 (1) "이번 여행은 누구랑 함께 하실 예정이신가요?" 메시지를 추가

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

            <!-- 캘린더 입력 -->
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

            <!-- 버튼 그룹 -->
            {#if message.buttons}
              <div class="button-wrapper">

                {#each message.buttons as button}
                  <button
                    class="chat-btn"
                    on:click={() => handleButtonClick(button.text)}
                    >{button.text}</button
                  >


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

  /* 챗봇 창 */
  .chatbot-window {
    height: 75vh;
    overflow-y: auto;
    background-color: #ffecb9;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  /* 헤더 스타일 */
  .chat-header {
    text-align: center;
    color: #000;
    padding: 10px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px 10px 0 0;
    background-color: #f8d17d;
  }

  /* 메시지 래퍼 */
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

  /* 봇 프로필 */
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
    font-family: "Arial", sans-serif;
  }

  /* 메시지 박스 */
  .message-bot {
    background-color: white;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 70%;
    font-size: 14px;
    margin-bottom: 10px;

    word-wrap: break-word;


  .message-user {
    background-color: #d1e7dd;
    color: #000;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 70%;
    font-size: 14px;
    text-align: right;
  }

  /* 버튼 스타일 */
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
    border: 1px solid #ddd;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
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
  }


  .confirm-btn:hover {
    background-color: #f1f1f1;
  }

  /* 확인 버튼 */
  .confirm-btn {
    margin-top: 10px;
    transform: translate(90px, 0%);
  }

  /* 캘린더 입력 */
  .message-bot input[type="date"] {
    width: 100%;
    padding: 5px;
    margin-top: 5px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }

  /* 캘린더 메시지 스타일 */
  .calendar-message {
    max-width: 80%;
    word-wrap: break-word;
    text-align: center;
    margin: 10px 0;
  }
</style>