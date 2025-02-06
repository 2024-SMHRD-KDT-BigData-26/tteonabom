const selectedData = {};

export function initializeChat(callback) {
    const initialMessages = [
        {
            type: "bot",
            text: "안녕하세요! 무엇을 도와드릴까요?",
            buttons: [
                { text: "여행 일정 추천", action: "schedule" },
                { text: "여행지 추천", action: "destination" },
                { text: "쇼핑몰 추천", action: "shopping" }
            ]
        }
    ];

    callback(initialMessages);
}

export function sendMessage(messages, text, setShowCalendar, updateMessages, selectedData) {
    let botResponse = null;
    let updatedMessages = [...messages, { type: "user", text }];
    // 1. 여행 일정 추천
    if (text === "여행 일정 추천") {
        botResponse = {
            type: "bot",
            text: "(1/5) 언제부터 언제까지 여행하실 계획이신가요?",
            showCalendar: true,
        };
        setShowCalendar(true);
    } else if (text.startsWith("📅 여행 일정:")) {
        selectedData["여행 일정"] = text.replace("📅 여행 일정: ", "");
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
        selectedData["동반자"] = text;
        botResponse = {
            type: "bot",
            text: "(3/5) 여행하고 싶은 지역을 선택해주세요.",
            buttons: [
                { text: "수도권", action: "seoul" },
                { text: "강원권", action: "gangwon" },
                { text: "충청권", action: "chungcheong" },
                { text: "호남권", action: "honam" },
                { text: "영남권", action: "yeongnam" },
                { text: "제주권", action: "jeju" },
            ],
        };
    } else if (["수도권", "강원권", "충청권", "호남권", "영남권", "제주권"].includes(text)) {
        selectedData["목적지"] = text;
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
        selectedData["여행 스타일"] = text;
        botResponse = {
            type: "bot",
            text: "(5/5) 어떤 일정 스타일을 원하시나요?",
            buttons: [
                { text: "타이트한 일정", action: "tight" },
                { text: "여유로운 일정", action: "relaxed" },
            ],
        };
    } else if (["타이트한 일정", "여유로운 일정"].includes(text)) {
        selectedData["일정 스타일"] = text;

        if (!selectedData["여행 일정"]) {
            console.error("❌ 여행 일정이 설정되지 않았습니다.");
            return;
        }

        setTimeout(() => {
            updateMessages({
                type: "bot",
                text: `📌 여행 정보 정리<br>- 여행 일정: ${selectedData["여행 일정"]}<br>- 목적지: ${selectedData["목적지"]}<br>- 동반자: ${selectedData["동반자"]}<br>- 여행 스타일: ${selectedData["여행 스타일"]}<br>- 일정 스타일: ${selectedData["일정 스타일"]}`
            });
        }, 0);

        const [startDate, endDate] = selectedData["여행 일정"].split(" ~ ");
        const start = new Date(startDate.replace(/\//g, "-"));
        const end = new Date(endDate.replace(/\//g, "-"));
        const daysDiff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;

        let delay = 500;
        for (let i = 0; i < daysDiff; i++) {
            setTimeout(() => {
                const currentDate = new Date(start);
                currentDate.setDate(start.getDate() + i);
                const formattedDate = currentDate.toISOString().split("T")[0];

                updateMessages({ type: "bot", text: `📅 ${formattedDate} 일정을 계획 중입니다...` });

                if (i === daysDiff - 1) {
                    setTimeout(() => {
                        updateMessages({
                            type: "bot",
                            text: "추천한 일정이 마음에 드셨나요?",
                            buttons: [
                                { text: "일정 다운로드", action: "download" },
                                { text: "채팅 내용 저장", action: "save_chat" },
                                { text: "처음으로 돌아가기", action: "restart" },
                            ],
                        });
                    }, 500);
                }
            }, delay);
            delay += 500;
        }
        // 2. 여행지 추천
    } else if (text === "여행지 추천") {
        botResponse = {
            type: "bot",
            text: "여행지를 추천 드릴게요! 어떤 여행으로 추천 드릴까요?",
            buttons: [
                { text: "엑티비티/체험", action: "destination_activity" },
                { text: "힐링/관광", action: "destination_healing" },
                { text: "핫플레이스", action: "destination_hotplace" },
            ],
        };
    } else if (["엑티비티/체험", "힐링/관광", "핫플레이스"].includes(text)) {
        selectedData["여행 스타일"] = text;
        botResponse = {
            type: "bot",
            text: "누구랑 함께 떠나시나요?",
            buttons: [
                { text: "가족", action: "destination_family" },
                { text: "연인", action: "destination_couple" },
                { text: "친구", action: "destination_friends" },
                { text: "혼자", action: "destination_alone" },
            ],
        };
    } else if (["가족", "연인", "친구", "혼자"].includes(text)) {
        selectedData["동반자"] = text;
        botResponse = {
            type: "bot",
            text: `"${text}" 떠나시는군요? 지역을 선택해주세요!`,
            buttons: [
                { text: "수도권", action: "destination_seoul" },
                { text: "강원권", action: "destination_gangwon" },
                { text: "충청권", action: "destination_chungcheong" },
                { text: "호남권", action: "destination_honam" },
                { text: "영남권", action: "destination_yeongnam" },
                { text: "제주권", action: "destination_jeju" },
            ],
        };
    } else if (["수도권", "강원권", "충청권", "호남권", "영남권", "제주권"].includes(text)) {
        selectedData["지역"] = text;

        botResponse = {
            type: "bot",
            text: `"${text}"의 여행지 목록입니다! 🏝️`,
        };

        setTimeout(() => {
            updateMessages({
                type: "bot",
                text: "추천 여행지가 마음에 드시나요?",
                buttons: [
                    { text: "여행지 추천 다시 받기", action: "destination_retry" },
                    { text: "여행지 추천", action: "destination_recommend" },
                    { text: "처음으로 돌아가기", action: "restart" },
                ],
            });
        }, 500);
    } else if (text === "여행지 추천 다시 받기") {
        botResponse = {
            type: "bot",
            text: "다시 추천을 진행하겠습니다! 어떤 여행으로 추천 드릴까요?",
            buttons: [
                { text: "엑티비티/체험", action: "destination_activity" },
                { text: "힐링/관광", action: "destination_healing" },
                { text: "핫플레이스", action: "destination_hotplace" },
            ],
        };
    } else if (text === "처음으로 돌아가기") {
        botResponse = {
            type: "bot",
            text: "처음 화면으로 돌아갑니다!",
            buttons: [
                { text: "여행 일정 추천", action: "schedule_recommend" },
                { text: "여행지 추천", action: "destination_recommend" },
                { text: "쇼핑몰 추천", action: "shopping_recommend" }
            ],
        };
    }
    else if (text === "쇼핑몰 추천") {
        botResponse = {
            type: "bot",
            text: "어떤 테마의 쇼핑몰을 찾고 계신가요?",
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
        };
    }

    if (botResponse) {
        updatedMessages.push(botResponse);
    }

    return { updatedMessages };
}

export function scrollToBottom() {
    setTimeout(() => {
        const chatWindow = document.getElementById("chatWindow");
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }, 100);
}
