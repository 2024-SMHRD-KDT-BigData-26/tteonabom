// myChatlogView.js

export function getChatMessages() {
    return [
      {
        type: "bot",
        text: "안녕하세요! 여행의 시작부터 끝까지 떠나봄의 여행AI 봄봄입니다! AI가 당신의 완벽한 여행을 도와드립니다!",
      },
      {
        type: "user",
        text: "여행 일정 추천",
      },
      {
        type: "bot",
        text: "(1/5) 언제부터 언제까지 여행하실 계획이신가요?",
      },
      {
        type: "user",
        text: "2025.02.20 ~ 2025.02.25",
      },
      {
        type: "bot",
        text: "(2/5) 이번 여행은 누구랑 함께 하실 예정이신가요?",
      },
      {
        type: "user",
        text: "가족",
      },
      {
        type: "bot",
        text: "(3/5) 이번 여행은 가족이랑 가시는군요? 여행하고 싶은 지역을 선택해주세요.",
      },
      {
        type: "user",
        text: "수도권",
      },
      {
        type: "bot",
        text: "(4/5) 선호하는 여행 스타일을 선택해주세요!",
      },
      {
        type: "user",
        text: "힐링/관광",
      },
      {
        type: "bot",
        text: "(5/5) 어떤 일정 스타일을 원하시나요?",
      },
      {
        type: "user",
        text: "여유로운 일정",
      },
      {
        type: "bot",
        text: "여행 계획이 완성되었습니다! 즐거운 여행 되세요!",
      },
    ];
  }
  