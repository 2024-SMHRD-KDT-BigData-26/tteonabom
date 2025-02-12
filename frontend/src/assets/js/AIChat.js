const selectedData = {};

const shoppingMallLinks = {
    등산: [
        { name: "디스커버리", url: "https://www.discovery-expedition.com/" },
        { name: "K2", url: "https://www.k2.co.kr/" },
        { name: "가야미", url: "https://www.gayamy.co.kr/index.html" },
        { name: "고캠프", url: "https://www.gocamp.co.kr/shop/main/index.php" },
        { name: "락8848", url: "https://www.rock8848.com/main/index.php" },
        { name: "액트", url: "https://actc.co.kr/index.html" },
        { name: "예스마운틴", url: "https://www.yesmountain.com/" }
    ],
    물놀이: [
        { name: "아레나", url: "https://www.arena.co.kr/" },
        { name: "배럴", url: "https://summer.barrel.co.kr/" },
        { name: "레스틴온오션", url: "https://restincocean.com/shop" },
        { name: "스윔어바웃", url: "https://brand.naver.com/swimabout" },
        { name: "가나수원", url: "https://swim.co.kr/index.html" },
        { name: "200bar", url: "https://200bar.shop/main/index" },
        { name: "단비몰", url: "https://smartstore.naver.com/haechy" },
        { name: "미노서프", url: "https://minossurf.com/" }
    ],
    서핑: [
        { name: "허니서프", url: "https://www.honeysurf.co.kr/" },
        { name: "서프코드", url: "https://surfcode.co.kr/" },
        { name: "서퍼스", url: "https://www.surfers.co.kr/" },
        { name: "오썸머", url: "https://osummer.co.kr/index.html" },
        { name: "서프존", url: "https://surfzone.co.kr/" },
        { name: "얼라이브스킴", url: "https://aliveskim.com/" },
        { name: "플라이비치", url: "https://www.flybeach.co.kr/" }
    ],
    스키: [
        { name: "피닉스 스키", url: "https://www.phoenixhnr.co.kr/" },
        { name: "휘닉스파크", url: "https://www.wellihillipark.com/" },
        { name: "봄레포츠", url: "https://bomnasports.com/" },
        { name: "에스엠스키", url: "https://m.sportscore.co.kr/" },
        { name: "피닉스스포츠", url: "https://phoenixsports.co.kr/index.html" },
        { name: "스노우뱅크", url: "https://snowbank.net/index.html" }
    ],
    여행용품: [
        { name: "트래블메이트", url: "https://www.travelmate.co.kr/" },
        { name: "샘소나이트", url: "https://www.samsonite.co.kr/" },
        { name: "몬타나스포츠", url: "https://montanak.co.kr/" },
        { name: "트래블로드", url: "https://travelload.co.kr/" },
        { name: "고고캠핑", url: "https://m.gogcamp.co.kr/#enp_mbris" },
        { name: "인블루", url: "https://www.in-travel.co.kr/index.html" },
        { name: "신비로드", url: "https://smartstore.naver.com/sinbiroad" }
    ],
    자전거: [
        { name: "스페셜라이즈드", url: "https://www.specialized.com/" },
        { name: "자이언트", url: "https://www.giant-bicycles.com/" },
        { name: "자이크", url: "https://shop1.jaike.cafe24.com/" },
        { name: "고르고타고", url: "https://www.gorogotago.com/" },
        { name: "바이오인", url: "https://www.tradeinn.com/bikeinn/ko" },
        { name: "오딜로", url: "https://www.odvelo.com/" },
        { name: "자출사닷컴", url: "https://www.jachulsa.com/index.html" }
    ],
    카메라: [
        { name: "준카메라", url: "https://juncamera.co.kr/index.html" },
        { name: "반도카메라", url: "https://bandocamera.co.kr/index.html" },
        { name: "거성카메라", url: "https://geosungcamera.com/index.html" },
        { name: "줌인", url: "https://www.zoomin.co.kr/" },
        { name: "부성카메라", url: "https://boosungcamera.co.kr/" }
    ],
    캠핑: [
        { name: "인디에어", url: "https://smartstore.naver.com/inthea" },
        { name: "이아웃도어", url: "https://www.eoutdoors.co.kr/index.html" },
        { name: "오캠몰", url: "https://www.ocamall.com/" },
        { name: "맥킨리", url: "http://www.e-mckinley.co.kr/index.html" },
        { name: "캠핑파파", url: "https://www.campingpapa.co.kr/shop/main/index.php" }
    ],
    낚시: [
        { name: "낚시밸리", url: "https://fishvalley.com/main/index.php" },
        { name: "야멧피싱", url: "https://imfishing.kr/" },
        { name: "싸파몰", url: "https://sapa.co.kr/" },
        { name: "텔낚시", url: "https://www.ytfishing.co.kr/" },
        { name: "가자낚시", url: "https://ok1717.com/" }
    ]
};

// 엑셀 다운로드 처리 함수
export async function downloadExcelFile(chatId = 91) {  // 기본값을 91로 설정
    if (!chatId) {
        console.error("엑셀 다운로드 실패: 채팅방 ID(chatId)가 제공되지 않았습니다.");
        return;
    }
    try {
        // chatId가 91일 경우, CROOM_IDX를 192로 설정하여 요청
        if (chatId === 91) {
            chatId = 192; // CROOM_IDX에 맞춰서 192로 설정
        }

        const response = await fetch(`http://localhost:9000/chat/download/${chatId}`, {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            throw new Error('엑셀 다운로드 실패');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');

        link.href = url;
        link.download = `gpt_response_${chatId}.xlsx`;
        link.click();

        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error("엑셀 다운로드 오류:", error);
    }
}



// 채팅 내용 저장 함수
export async function saveChatContent(croomId, userId) {
    if (!croomId || !userId) {
        console.error("저장 실패: croomId와 userId가 모두 제공되어야 합니다.");
        return;
    }
    try {
        const response = await fetch('http://localhost:9000/chat/save', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ CROOM_IDX: croomId, USER_ID: userId }),
        });

        if (!response.ok) {
            throw new Error('저장 실패');
        }

        const data = await response.json();
        console.log('채팅 내용 저장 성공:', data);
    } catch (error) {
        console.error("저장 오류:", error);
    }
}

// API 요청 함수
export async function fetchDataFromAPI(url, requestData) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API 호출 실패: ${errorText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("API 호출 오류:", error);
        return { error: "서버와의 연결에 문제가 발생했습니다. 잠시 후 다시 시도해주세요." };
    }
}
// 챗봇 처음
export function initializeChat(callback) {
    const initialMessages = [
        {
            type: "bot",
            text: "안녕하세요!<br>여행의 시작부터 끝까지<br>떠나봄의 여행AI 떠나봄입니다!<br><br>AI가 당신의 완벽한 여행을 도와드립니다!<br><br>아래에서 원하는 버튼을 클릭해주세요!",
            buttons: [
                { text: "여행 일정 추천", action: "schedule" },
                { text: "여행지 추천", action: "destination" },
                { text: "쇼핑몰 추천", action: "shopping" }
            ]
        }
    ];
    callback(initialMessages);
}
// 챗봇 초기화
export function sendMessage(messages, text, setShowCalendar, updateMessages, selectedData) {
    let botResponse = null;
    let updatedMessages = [...messages, { type: "user", text }];

    console.log("입력된 text 값:", text); // ✅ 현재 입력된 값 디버깅

    if (text === "처음으로 돌아가기") {
        console.log("🔄 처음으로 돌아가기 실행됨!"); // 디버깅 로그
        Object.keys(selectedData).forEach(key => delete selectedData[key]);
        selectedData["mode"] = null;
        updateMessages([]); // 기존 메시지 초기화

        const initialMessages = [
            {
                type: "bot",
                text: "안녕하세요!<br>여행의 시작부터 끝까지<br>떠나봄의 여행AI 떠나봄입니다!<br><br>AI가 당신의 완벽한 여행을 도와드립니다!<br><br>아래에서 원하는 버튼을 클릭해주세요!",
                buttons: [
                    { text: "여행 일정 추천", action: "schedule" },
                    { text: "여행지 추천", action: "destination" },
                    { text: "쇼핑몰 추천", action: "shopping" }
                ]
            }
        ];

        updateMessages(initialMessages);
        return { updatedMessages: initialMessages }; // 초기 메시지를 반환
    }



    /*** ✅ 1. 여행 일정 추천 ***/
    if (text === "여행 일정 추천") {
        botResponse = {
            type: "bot",
            text: "여행일정 추천을 선택하셨군요! <br>일정을 추천하기 위해 몇가지 질문에 답변해주세요.<br><br>(1/5) 언제부터 언제까지 여행하실 계획이신가요?",
            showCalendar: true,
        };
        setShowCalendar(true);
    } else if (text.startsWith("📅 여행 일정:")) {
        selectedData["여행 일정"] = text.replace("📅 여행 일정:<br> ", "");
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
    // ✅ 일정 스타일 선택 후 자동 요약 및 날짜별 일정 생성
    else if (["타이트한 일정", "여유로운 일정"].includes(text) && selectedData["여행 일정"]) {
        selectedData["일정 스타일"] = text;

        // 사용자 입력 데이터 정리 메시지
        setTimeout(() => {
            updateMessages({
                type: "bot",
                text: `📌 여행 정보 정리<br>- 여행 일정: ${selectedData["여행 일정"]}<br>- 목적지: ${selectedData["목적지"]}<br>- 동반자: ${selectedData["동반자"]}<br>- 여행 스타일: ${selectedData["여행 스타일"]}<br>- 일정 스타일: ${selectedData["일정 스타일"]}`
            });
        }, 0);

        const loadingMessage = { type: "bot", text: "⏳ 여행 일정을 추천하는 중입니다. 잠시만 기다려 주세요!" };
        updateMessages(loadingMessage);

        const USER_ID = "test_user_123";
        const [start_date, end_date] = selectedData["여행 일정"].split(" ~ ");
        const scheduleData = {
            USER_ID: USER_ID,
            TRAVEL_DATA: {
                start_date: start_date.trim(),
                end_date: end_date.trim(),
                companion: selectedData["동반자"],
                region: selectedData["목적지"],
                style: selectedData["여행 스타일"],
                schedule: selectedData["일정 스타일"]
            }
        };

        fetchDataFromAPI("http://localhost:9000/chat", scheduleData).then((result) => {
            messages = messages.filter(msg => msg !== loadingMessage);

            if (result && result.gpt_response) {
                let cleanedResponse = result.gpt_response
                    .replace(/```html/g, '')  // ✅ ``html 제거
                    .replace(/```/g, '')       // ✅ ``` (닫는 코드 블록) 제거
                    .trim();                   // ✅ 앞뒤 공백 제거
                updateMessages({ type: "bot", text: cleanedResponse });

                // result에 croom_id가 존재하는지 확인하고, 해당 값을 시스템 메시지로 추가
                let croomId = 192;  // croom_id 값을 192로 설정
                if (!messages.some(msg => msg.type === "system" && msg.croom_id)) {
                    updateMessages({ type: "system", croom_id: croomId });
                }


                updateMessages({
                    type: "bot",
                    text: "추천 일정이 마음에 드셨나요?",
                    buttons: [
                        { text: "일정 다운로드", action: "download" },
                        { text: "채팅 내용 저장", action: "save_chat" },
                        { text: "처음으로 돌아가기", action: "restart" },
                    ],
                });
            } else {
                updateMessages({
                    type: "bot",
                    text: "일정을 생성하지 못했습니다. 다시 시도해주세요.",
                    buttons: [{ text: "처음으로 돌아가기", action: "restart" }],
                });
            }
        });


    }


    // 2. 여행지 추천
    else if (text === "여행지 추천") {
        botResponse = {
            type: "bot",
            text: "어떤 여행으로 추천 드릴까요?",
            buttons: [
                { text: "엑티비티, 체험", action: "recommend_activity" },
                { text: "힐링, 관광", action: "recommend_healing" },
                { text: "핫플레이스", action: "recommend_hotplace" },
                { text: "먹거리", action: "recommend_food" },
            ],
        };
    } else if (["엑티비티, 체험", "힐링, 관광", "핫플레이스", "먹거리"].includes(text)) {
        selectedData["여행 테마"] = text;
        botResponse = {
            type: "bot",
            text: "누구와 함께 떠나시나요?",
            buttons: [
                { text: "가족", action: "recommend_family" },
                { text: "연인", action: "recommend_couple" },
                { text: "친구", action: "recommend_friends" },
                { text: "혼자", action: "recommend_alone" },
            ],
        };
    } else if (["가족", "연인", "친구", "혼자"].includes(text)) {
        selectedData["동반자"] = text;
        botResponse = {
            type: "bot",
            text: `${text} 떠나시는군요! 지역을 선택해주세요!`,
            buttons: [
                { text: "수도권", action: "recommend_seoul" },
                { text: "강원권", action: "recommend_gangwon" },
                { text: "충청권", action: "recommend_chungcheong" },
                { text: "호남권", action: "recommend_honam" },
                { text: "영남권", action: "recommend_yeongnam" },
                { text: "제주권", action: "recommend_jeju" },
            ],
        };
    } else if (["수도권", "강원권", "충청권", "호남권", "영남권", "제주권"].includes(text)) {
        selectedData["목적지"] = text;
    
        updateMessages({ type: "bot", text: "추천 여행지를 불러오는 중입니다... 🚀" });
    
        // ✅ FastAPI 요청 데이터
        const recommendData = {
            USER_ID: "test_user_123",
            COMPANION: selectedData["동반자"],
            THEME: selectedData["여행 테마"],
            REGION: selectedData["목적지"]
        };
    
        console.log("📌 [프론트엔드] 요청 데이터:", JSON.stringify(recommendData, null, 2));
    
        fetchDataFromAPI("http://localhost:9000/travel/recommend", recommendData).then((result) => {
            if (result && result.gpt_response) {
                let cleanedResponse = result.gpt_response
                    .replace(/```html/g, '')  // ✅ ``html 제거
                    .replace(/```/g, '')       // ✅ ``` (닫는 코드 블록) 제거
                    .trim();                   // ✅ 앞뒤 공백 제거
    
                updateMessages({ type: "bot", text: cleanedResponse });
    
                updateMessages({
                    type: "bot",
                    text: "추천 여행지가 마음에 드셨나요?",
                    buttons: [
                        { text: "추천 다시 받기", action: "recommend_retry" },
                        { text: "처음으로 돌아가기", action: "restart" },
                    ],
                });
            }
        });
    } else if (text === "추천 다시 받기") {
        updateMessages({ type: "bot", text: "새로운 여행지를 추천하는 중입니다. 잠시만 기다려주세요... 🚀" });
    
        const recommendData = {
            USER_ID: "test_user_123",
            COMPANION: selectedData["동반자"],
            THEME: selectedData["여행 테마"],
            REGION: selectedData["목적지"]
        };
    
        console.log("📌 [프론트엔드] 다시 추천 요청 데이터:", JSON.stringify(recommendData, null, 2));
    
        fetchDataFromAPI("http://localhost:9000/travel/recommend", recommendData).then((result) => {
            if (result && result.gpt_response) {
                let cleanedResponse = result.gpt_response
                    .replace(/```html/g, '')  // ✅ ``html 제거
                    .replace(/```/g, '')       // ✅ ``` (닫는 코드 블록) 제거
                    .trim();                   // ✅ 앞뒤 공백 제거
    
                updateMessages({ type: "bot", text: cleanedResponse });
    
                updateMessages({
                    type: "bot",
                    text: "새로운 추천 여행지는 마음에 드셨나요?",
                    buttons: [
                        { text: "추천 다시 받기", action: "recommend_retry" },
                        { text: "처음으로 돌아가기", action: "restart" }
                    ]
                });
            } else {
                updateMessages({
                    type: "bot",
                    text: "새로운 추천 여행지를 가져오지 못했습니다. 다시 시도해주세요.",
                    buttons: [{ text: "처음으로 돌아가기", action: "restart" }]
                });
            }
        }).catch(error => {
            console.error("🚨 추천 다시 받기 오류:", error);
            updateMessages({
                type: "bot",
                text: "여행지 추천 중 오류가 발생했습니다. 다시 시도해주세요.",
                buttons: [{ text: "처음으로 돌아가기", action: "restart" }]
            });
        });
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
    // ✅ 사용자가 특정 테마 선택 시 → 랜덤한 3개 쇼핑몰 목록 출력
    else if (["등산", "물놀이", "서핑", "스키", "여행용품", "자전거", "카메라", "캠핑", "낚시"].includes(text)) {
        selectedData["쇼핑 테마"] = text;

        let malls = shoppingMallLinks[text];
        let randomMalls = malls.sort(() => 0.5 - Math.random()).slice(0, 3); // 배열을 무작위로 섞고 3개 선택

        let mallList = randomMalls
            .map(mall => `${mall.name}<br><a href="${mall.url}" target="_blank">${mall.url}</a>`)
            .join("<br><br>");

        botResponse = {
            type: "bot",
            text: ` "${text}"과 관련된 쇼핑몰 목록입니다!<br>필요한 물품들을 쇼핑해보세요!😀<br><br>${mallList}`,
            buttons: [
                { text: "다른 쇼핑몰 목록 보기", action: "shopping" },
                { text: "다시 추천 받기", action: "shopping_retry" },
                { text: "처음으로 돌아가기", action: "restart" }
            ]
        };
    }
    // ✅ "다시 추천 받기" 클릭 시 → 기존에 선택한 쇼핑 테마의 목록을 랜덤으로 다시 출력
    else if (text === "다시 추천 받기" && selectedData["쇼핑 테마"]) {
        let theme = selectedData["쇼핑 테마"];
        let malls = shoppingMallLinks[theme];
        let randomMalls = malls.sort(() => 0.5 - Math.random()).slice(0, 3); // 랜덤 3개 선택

        let mallList = randomMalls
            .map(mall => `${mall.name}<br><a href="${mall.url}" target="_blank">${mall.url}</a>`)
            .join("<br><br>");

        botResponse = {
            type: "bot",
            text: ` "${theme}"과 관련된 다른 쇼핑몰 목록입니다!<br>필요한 물품들을 쇼핑해보세요!😀<br><br>${mallList}`,
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
    }
    // ✅ 항상 반환값 보장
    return { updatedMessages };

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