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

    console.log("입력된 text 값:", text); // ✅ 현재 입력된 값 디버깅

    if (text === "처음으로 돌아가기") {
        console.log("🔄 처음으로 돌아가기 실행됨!"); // ✅ 디버깅용 로그
        Object.keys(selectedData).forEach(key => delete selectedData[key]);
        selectedData["mode"] = null;
        updateMessages([]); // ✅ 기존 메시지 목록을 비움

        // ✅ 초기 메시지를 즉시 설정 (버튼이 나오도록)
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

        updateMessages(initialMessages); // ✅ 즉시 초기 메시지 업데이트
        return { updatedMessages: initialMessages }; // ✅ 항상 객체 반환
    }


    /*** ✅ 1. 여행 일정 추천 ***/
    if (text === "여행 일정 추천") {
        botResponse = {
            type: "bot",
            text: "여행일정 추천을 선택하셨군요! 일정을 추천하기 위해 몇가지 질문에 답변해주세요.(1/5) 언제부터 언제까지 여행하실 계획이신가요?",
            showCalendar: true,
        };
        setShowCalendar(true);
    } else if (text.startsWith("📅 여행 일정:")) {
        selectedData["여행 일정"] = text.replace("📅 여행 일정: ", "");
        botResponse = {
            type: "bot",
            text: "(2/5) 이번 여행은 누구랑 함께 하실 예정이신가요?",
            buttons: [
                { text: "가족", action: "schedule_family" },
                { text: "연인", action: "schedule_couple" },
                { text: "친구", action: "schedule_friends" },
                { text: "혼자", action: "schedule_alone" },
            ],
        };
    } else if (["가족", "연인", "친구", "혼자"].includes(text) && selectedData["여행 일정"]) {
        selectedData["동반자"] = text;
        botResponse = {
            type: "bot",
            text: "(3/5) 여행하고 싶은 지역을 선택해주세요.",
            buttons: [
                { text: "수도권", action: "schedule_seoul" },
                { text: "강원권", action: "schedule_gangwon" },
                { text: "충청권", action: "schedule_chungcheong" },
                { text: "호남권", action: "schedule_honam" },
                { text: "영남권", action: "schedule_yeongnam" },
                { text: "제주권", action: "schedule_jeju" },
            ],
        };
    } else if (["수도권", "강원권", "충청권", "호남권", "영남권", "제주권"].includes(text) && selectedData["여행 일정"]) {
        selectedData["목적지"] = text;
        botResponse = {
            type: "bot",
            text: "(4/5) 선호하는 여행 스타일을 선택해주세요!",
            buttons: [
                { text: "엑티비티/체험", action: "schedule_activity" },
                { text: "힐링/관광", action: "schedule_healing" },
                { text: "핫플레이스", action: "schedule_hotplace" },
            ],
        };
    } else if (["엑티비티/체험", "힐링/관광", "핫플레이스"].includes(text) && selectedData["여행 일정"]) {
        selectedData["여행 스타일"] = text;
        botResponse = {
            type: "bot",
            text: "(5/5) 어떤 일정 스타일을 원하시나요?",
            buttons: [
                { text: "타이트한 일정", action: "tight" },
                { text: "여유로운 일정", action: "relaxed" },
            ],
        };
    }
    /*** ✅ 일정 스타일 선택 후 자동 요약 및 날짜별 일정 생성 ***/
    else if (["타이트한 일정", "여유로운 일정"].includes(text) && selectedData["여행 일정"]) {
        selectedData["일정 스타일"] = text;

        setTimeout(() => {
            updateMessages({
                type: "bot",
                text: `📌 여행 정보 정리<br>- 여행 일정: ${selectedData["여행 일정"]}<br>- 목적지: ${selectedData["목적지"]}<br>- 동반자: ${selectedData["동반자"]}<br>- 여행 스타일: ${selectedData["여행 스타일"]}<br>- 일정 스타일: ${selectedData["일정 스타일"]}`
            });
        }, 0);

        // ✅ 날짜별 일정 생성
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
    }

    /*** ✅ 2. 여행지 추천 ***/
    else if (text === "여행지 추천") {
        botResponse = {
            type: "bot",
            text: "여행지를 추천 드릴게요! 어떤 여행으로 추천 드릴까요?",
            buttons: [
                { text: "엑티비티/체험", action: "destination_activity" },
                { text: "힐링/관광", action: "destination_healing" },
                { text: "핫플레이스", action: "destination_hotplace" },
            ],
        };
    } else if (["엑티비티/체험", "힐링/관광", "핫플레이스"].includes(text) && !selectedData["여행 일정"]) {
        selectedData["여행지 스타일"] = text; // ✅ 여행지 추천 흐름에서는 여행 스타일과 다른 변수 사용
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
    } else if (["가족", "연인", "친구", "혼자"].includes(text) && selectedData["여행지 스타일"]) {
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
    } else if (["수도권", "강원권", "충청권", "호남권", "영남권", "제주권"].includes(text) && selectedData["여행지 스타일"]) {
        selectedData["여행 지역"] = text;
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
    }
    // 3. 쇼핑몰 추천하기
     /*** ✅ 쇼핑몰 추천 기능 ***/
     if (text === "쇼핑몰 추천" || text === "다른 쇼핑몰 목록 보기") {
        // ✅ "다른 쇼핑몰 목록 보기" 클릭 시 동일한 코드 실행
        botResponse = {
            type: "bot",
            text: "어떤 테마의 쇼핑몰을 찾고 계신가요?",
            buttons: [
                { text: "등산", action: "shopping_mountain" },
                { text: "물놀이", action: "shopping_swimming" },
                { text: "서핑", action: "shopping_surfing" },
                { text: "스키", action: "shopping_ski" },
                { text: "여행용품", action: "shopping_travel" },
                { text: "자전거", action: "shopping_bicycle" },
                { text: "카메라", action: "shopping_camera" },
                { text: "캠핑", action: "shopping_camping" },
                { text: "낚시", action: "shopping_fishhook" }
            ],
        };
    } 
    // ✅ 사용자가 특정 테마 선택 시 → 쇼핑몰 목록 출력
    else if (["등산", "물놀이", "서핑", "스키", "여행용품", "자전거", "카메라", "캠핑", "낚시"].includes(text)) {
        selectedData["쇼핑 테마"] = text;

        let mallList = shoppingMallLinks[text]
            .map(mall => `<a href="${mall.url}" target="_blank">${mall.name}</a>`)
            .join("<br>");

        botResponse = {
            type: "bot",
            text: `✅ "${text}"과 관련된 쇼핑몰 목록입니다!🛍️<br>필요한 물품들을 쇼핑해보세요!😀<br>${mallList}`,
            buttons: [
                { text: "다른 쇼핑몰 목록 보기", action: "shopping" }, // ✅ 쇼핑 테마 선택 화면으로 이동
                { text: "다시 추천 받기", action: "shopping_retry" }, 
                { text: "처음으로 돌아가기", action: "restart" }
            ]
        };
    } 
    // ✅ "다시 추천 받기" 클릭 시 → 기존에 선택한 쇼핑 테마의 목록을 다시 출력
    else if (text === "다시 추천 받기" && selectedData["쇼핑 테마"]) {
        let theme = selectedData["쇼핑 테마"];
        let mallList = shoppingMallLinks[theme]
            .map(mall => `<a href="${mall.url}" target="_blank">${mall.name}</a>`)
            .join("<br>");

        botResponse = {
            type: "bot",
            text: `✅ "${theme}"과 관련된 다른 쇼핑몰 목록입니다!🛍️<br>필요한 물품들을 쇼핑해보세요!😀<br>${mallList}`,
            buttons: [
                { text: "다른 쇼핑몰 목록 보기", action: "shopping" }, // ✅ 쇼핑 테마 선택 화면으로 이동
                { text: "다시 추천 받기", action: "shopping_retry" },
                { text: "처음으로 돌아가기", action: "restart" }
            ]
        };
    }

    // ✅ botResponse가 존재하는 경우만 메시지 업데이트
    if (botResponse) {
        updatedMessages.push(botResponse);
        return { updatedMessages };
    }
}

// ✅ 챗봇 스크롤 자동 내리기
export function scrollToBottom() {
    setTimeout(() => {
        const chatWindow = document.getElementById("chatWindow");
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }, 100);
}