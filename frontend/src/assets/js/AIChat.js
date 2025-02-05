export function initializeChat(setMessages) {
    const initialMessages = [
        {
            type: "bot",
            text: "안녕하세요! 여행의 시작부터 끝까지 떠나봄의 여행AI 봄봄입니다! AI가 당신의 완벽한 여행을 도와드립니다! 아래에서 원하는 추천 버튼을 눌러주세요!",
            buttons: [
                { text: "여행 일정 추천", action: "recommendSchedule" },
                { text: "여행지 추천", action: "recommendPlace" },
                { text: "쇼핑몰 추천", action: "recommendShopping" },
            ],
        },
    ];
    setMessages(initialMessages);
}

/* 여행 일정 추천 & 여행지 추천 */
export function sendMessage(messages, text, setShowCalendar) {
    let botResponse = null;

    // 여행 일정 추천
    if (text === "여행 일정 추천") {
        botResponse = {
            type: "bot",
            text: "(1/5) 언제부터 언제까지 여행하실 계획이신가요?",
            buttons: [],
            showCalendar: true,
        };
        setShowCalendar(true);
    } else if (text.startsWith("📅 여행 일정:")) {
        botResponse = {
            type: "bot",
            text: "(2/5) 이번 여행은 누구랑 함께 하실 예정이신가요?",
            buttons: [
                { text: "가족", action: "family" },
                { text: "연인", action: "couple" },
                { text: "친구", action: "friends" },
                { text: "혼자", action: "alone" },
            ],
        };
    } else if (["가족", "연인", "친구", "혼자"].includes(text)) {
        botResponse = {
            type: "bot",
            text: `(3/5) 이번 여행은 ${text}이랑 가시는군요? 여행하고 싶은 지역을 선택해주세요.`,
            buttons: [
                { text: "수도권", action: "seoul" },
                { text: "서부권", action: "west" },
                { text: "동부권", action: "east" },
                { text: "제주권", action: "jeju" },
            ],
        };
    } else if (["수도권", "서부권", "동부권", "제주권"].includes(text)) {
        botResponse = {
            type: "bot",
            text: "(4/5) 선호하는 여행 스타일을 선택해주세요!",
            buttons: [
                { text: "엑티비티/체험", action: "activity" },
                { text: "힐링/관광", action: "healing" },
                { text: "핫플레이스", action: "hotplace" },
            ],
        };
    } else if (["엑티비티/체험", "힐링/관광", "핫플레이스"].includes(text)) {
        botResponse = {
            type: "bot",
            text: "(5/5) 어떤 일정 스타일을 원하시나요?",
            buttons: [
                { text: "타이트한 일정", action: "tight" },
                { text: "여유로운 일정", action: "relaxed" },
            ],
        };
    } else if (["타이트한 일정", "여유로운 일정"].includes(text)) {
        updatedMessages = [...messages, { type: "user", text }];

        botResponse = {
            type: "bot",
            text: "멋진 선택이에요! 여행 일정을 추천해드릴게요. 잠시만 기다려주세요...",
        };
    }
    // 여행지 추천
    else if (text === "여행지 추천") {
        botResponse = {
            type: "bot",
            text: "여행지를 추천드릴게요! 어떤 여행으로 추천드릴까요?",
            buttons: [
                { text: "엑티비티/체험", action: "activity" },
                { text: "힐링/관광", action: "healing" },
                { text: "핫플레이스", action: "hotplace" },
                { text: "먹거리", action: "food" },
            ],
        };
    } else if (["엑티비티/체험", "힐링/관광", "핫플레이스", "먹거리"].includes(text)) {
        botResponse = {
            type: "bot",
            text: "누구랑 함께 떠나시나요?",
            buttons: [
                { text: "가족", action: "family" },
                { text: "연인", action: "couple" },
                { text: "친구", action: "friends" },
                { text: "혼자", action: "alone" },
            ],
        };
    } else if (["가족", "연인", "친구", "혼자"].includes(text)) {
        botResponse = {
            type: "bot",
            text: `${text}랑 떠나시는군요. 여행할 지역을 선택해주세요!`,
            buttons: [
                { text: "수도권", action: "seoul" },
                { text: "부산", action: "busan" },
                { text: "서부권", action: "west" },
                { text: "전남권", action: "jeonnam" },
                { text: "제주도", action: "jeju" },
            ],
        };
    }

    // 쇼핑몰 추천 
    else if (text === "쇼핑몰 추천") {
        botResponse = {
            type: "bot",
            text: "원하는 테마를 선택해주세요.",
            buttons: [
                { text: "등산", action: "mountain" },
                { text: "물놀이", action: "swimming" },
                { text: "서핑", action: "surfing" },
                { text: "수영복", action: "swimsuit" },
                { text: "스키", action: "ski" },
                { text: "여행용품", action: "travel" },
                { text: "자전거", action: "bicycle" },
                { text: "카메라", action: "camera" },
                { text: "캠핑", action: "camping" },
                { text: "낚시", action: "fishhook" },
            ],
        }
    };

    if (botResponse) {
        const updatedMessages = [...messages, { type: "user", text }, botResponse];
        return { updatedMessages };
    }

    return { updatedMessages: messages }; // 예외 상황에서 기존 메시지 유지
}

/* 스크롤 기능 */
export function scrollToBottom() {
    setTimeout(() => {
        const chatWindow = document.getElementById("chatWindow");
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }, 100);
}
