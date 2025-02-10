export async function requestChat(userId, travelData) {
    console.log("🟢 백엔드로 보낼 데이터:", JSON.stringify({
        USER_ID: userId,
        TRAVEL_DATA: travelData
    }));

    if (!userId || typeof userId !== "string") {
        console.error("🚨 오류: userId가 올바른 문자열이 아닙니다!", userId);
        throw new Error("잘못된 사용자 ID입니다.");
    }
    if (!travelData || typeof travelData !== "object" || Object.keys(travelData).length === 0) {
        console.error("🚨 오류: TRAVEL_DATA가 올바르지 않습니다!", travelData);
        throw new Error("잘못된 여행 데이터입니다.");
    }

    try {
        const response = await fetch("http://localhost:9000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                USER_ID: userId,
                TRAVEL_DATA: travelData
            })
        });

        if (!response.ok) {
            console.error("🚨 API 응답 오류:", response.status, await response.text());
            throw new Error("API 요청 실패");
        }

        return await response.json();
    } catch (error) {
        console.error("🚨 requestChat 함수에서 오류 발생:", error);
        throw error;
    }
}

const selectedData = {};

const shoppingMallLinks = {
    "등산": [
        { name: "디스커버리", url: "https://www.discovery-expedition.com/" },
        { name: "K2", url: "https://www.k2.co.kr/" }
    ],
    "물놀이": [
        { name: "아레나", url: "https://www.arena.co.kr/" },
        { name: "배럴", url: "https://summer.barrel.co.kr/" }
    ],
    "서핑": [
        { name: "허니서프", url: "https://www.honeysurf.co.kr/" },
        { name: "서프코드", url: "https://surfcode.co.kr/" }
    ],
    "스키": [
        { name: "피닉스 스키", url: "https://www.phoenixhnr.co.kr/" },
        { name: "휘닉스파크", url: "https://www.wellihillipark.com/" }
    ],
    "여행용품": [
        { name: "트래블메이트", url: "https://www.travelmate.co.kr/" },
        { name: "샘소나이트", url: "https://www.samsonite.co.kr/" }
    ],
    "자전거": [
        { name: "스페셜라이즈드", url: "https://www.specialized.com/" },
        { name: "자이언트", url: "https://www.giant-bicycles.com/" }
    ],
    "카메라": [
        { name: "캐논", url: "https://www.canon-ci.co.kr/" },
        { name: "니콘", url: "https://www.nikon-image.co.kr/" }
    ],
    "캠핑": [
        { name: "코베아", url: "https://www.kovea.co.kr/" },
        { name: "스노우라인", url: "https://www.snowline.co.kr/" }
    ],
    "낚시": [
        { name: "바낙스", url: "https://www.banax.co.kr/" },
        { name: "시마노", url: "https://fish.shimano.com/" }
    ]
};

export function initializeChat(callback) {
    const initialMessages = [
        {
            type: "bot",
            text: "안녕하세요! 여행의 시작부터 끝까지 떠나봄의 여행AI 떠나봄입니다! AI가 당신의 완벽한 여행을 도와드립니다! 아래에서 원하는 버튼을 클릭해주세요!",
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

    if (text === "여행 일정 추천") {
        botResponse = {
            type: "bot",
            text: "여행 일정 추천을 선택하셨군요! 여행 날짜를 선택해주세요.",
            showCalendar: true,
        };
        setShowCalendar(true);
    } else if (text.startsWith("📅 여행 일정:")) {
        selectedData["여행 일정"] = text.replace("📅 여행 일정: ", "");
        botResponse = {
            type: "bot",
            text: "GPT 응답을 생성 중입니다... 잠시만 기다려주세요.",
        };

        requestChat("test_user", selectedData)
            .then(response => {
                updateMessages({ type: "bot", text: response.gpt_response });
            })
            .catch(error => {
                console.error("GPT 응답을 가져오는 중 오류 발생:", error);
            });
    } else if (text === "쇼핑몰 추천") {
        botResponse = {
            type: "bot",
            text: "어떤 테마의 쇼핑몰을 찾고 계신가요?",
            buttons: Object.keys(shoppingMallLinks).map(theme => ({ text: theme, action: `shopping_${theme}` }))
        };
    } else if (Object.keys(shoppingMallLinks).includes(text)) {
        selectedData["쇼핑 테마"] = text;
        let mallList = shoppingMallLinks[text]
            .map(mall => `<a href="${mall.url}" target="_blank">${mall.name}</a>`)
            .join("<br>");

        botResponse = {
            type: "bot",
            text: `✅ "${text}"과 관련된 쇼핑몰 목록입니다!🛍️<br>${mallList}`,
            buttons: [
                { text: "다른 쇼핑몰 목록 보기", action: "shopping" },
                { text: "처음으로 돌아가기", action: "restart" }
            ]
        };
    } else if (text === "처음으로 돌아가기") {
        Object.keys(selectedData).forEach(key => delete selectedData[key]);

        botResponse = {
            type: "bot",
            text: "안녕하세요! 여행의 시작부터 끝까지 떠나봄의 여행AI 떠나봄입니다! AI가 당신의 완벽한 여행을 도와드립니다! 아래에서 원하는 버튼을 클릭해주세요!",
            buttons: [
                { text: "여행 일정 추천", action: "schedule" },
                { text: "여행지 추천", action: "destination" },
                { text: "쇼핑몰 추천", action: "shopping" }
            ]
        };
    }

    if (botResponse) {
        updatedMessages.push(botResponse);
        return { updatedMessages };
    }
}

export function scrollToBottom() {
    setTimeout(() => {
        const chatWindow = document.getElementById("chatWindow");
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }, 100);
}
