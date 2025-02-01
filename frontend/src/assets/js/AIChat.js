import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";

export function initializeChat() {
    return {
        initialMessages: [
            {
                text: "안녕하세요! 여행의 시작부터 끝까지 떠나봄의 AI 봄봄입니다!<br>AI가 당신의 완벽한 여행을 도와드립니다.<br><br>아래에서 원하는 추천 버튼을 클릭해주세요.",
                type: "bot",
                buttons: [
                    { text: "여행 일정 추천" },
                    { text: "여행지 추천" },
                    { text: "테마별 쇼핑몰 추천" }
                ]
            }
        ]
    };
}

export function sendMessage(messages, text) {
    let newMessages = [...messages, { text, type: "user" }];
    let response;
    let showDatePicker = false; 

    if (text === "여행 일정 추천") {
        response = {
            text: "여행 일정을 추천해드릴게요! 언제 떠나실 계획인가요?",
            type: "bot",
            buttons: [{ text: "날짜 선택" }]
        };
        showDatePicker = true;
    } else if (text === "날짜 선택") {
        return { updatedMessages: newMessages, showDatePicker: true };
    } else if (text.includes("~")) {
        response = {
            text: `선택하신 여행 기간: ${text} 입니다.<br>누구와 함께 여행하시나요?`,
            type: "bot",
            buttons: [
                { text: "가족" },
                { text: "친구" },
                { text: "연인" },
                { text: "혼자" }
            ]
        };
    }

    if (response) {
        newMessages.push(response);
    }

    return { updatedMessages: newMessages, showDatePicker };
}

export function setupDatePicker(onDateSelect) {
    setTimeout(() => {
        const chatWindow = document.getElementById("chatWindow");
        const datePickerWrapper = document.createElement("div");
        datePickerWrapper.id = "datePickerWrapper";
        chatWindow.appendChild(datePickerWrapper);

        flatpickr(datePickerWrapper, {
            mode: "range",
            dateFormat: "Y.m.d",
            minDate: "today",
            position: "auto",
            appendTo: datePickerWrapper,
            onClose: function (selectedDates, dateStr) {
                if (dateStr) {
                    onDateSelect(dateStr);
                }
            }
        }).open();
    }, 100);
}
