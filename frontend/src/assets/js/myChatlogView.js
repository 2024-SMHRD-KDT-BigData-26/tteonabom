export function getChatMessageById(chatId) {
  // 백엔드 API에서 데이터를 가져오는 부분 (예제용 JSON 데이터)
  return fetch(`/api/chatlog/${chatId}`)
    .then(response => response.json())
    .then(data => data.messages)
    .catch(error => {
      console.error("채팅 데이터를 불러오는 중 오류 발생:", error);
      return [];
    });
}