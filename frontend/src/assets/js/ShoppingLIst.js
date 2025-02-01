export function setupShoppingList(sortType = null) {
    console.log("쇼핑 리스트 JS가 실행되었습니다."); // 디버깅용 로그

    const likeButtons = document.querySelectorAll(".like-btn");
    const sortAlphabeticalButton = document.querySelector(".sort-text[on\\:click*='alphabetical']");
    const sortLikesButton = document.querySelector(".sort-text[on\\:click*='likes']");
    const cardContainer = document.querySelector(".card");
    const cards = Array.from(document.querySelectorAll(".card-body"));

    if (!cardContainer) {
        console.error("cardContainer를 찾을 수 없습니다.");
        return;
    }

    // 좋아요 버튼 클릭 이벤트 처리
    likeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const likeCountElement = button.previousElementSibling;
            let likes = parseInt(likeCountElement.textContent);
            const isLiked = button.getAttribute("data-liked") === "true";
            const heartImage = button.querySelector("img");

            if (isLiked) {
                likes--;
                button.setAttribute("data-liked", "false");
                heartImage.src = "/src/assets/img/heart.png";
            } else {
                likes++;
                button.setAttribute("data-liked", "true");
                heartImage.src = "/src/assets/img/full_heart.png";
            }

            likeCountElement.textContent = likes;
            const cardBody = button.closest(".card-body");
            cardBody.setAttribute("data-likes", likes);
        });
    });

    // 정렬 버튼 클릭 이벤트 처리
    if (sortAlphabeticalButton) {
        sortAlphabeticalButton.addEventListener("click", () => {
            setActiveButton(sortAlphabeticalButton, sortLikesButton);
            sortAlphabetically(cards, cardContainer);
        });
    }

    if (sortLikesButton) {
        sortLikesButton.addEventListener("click", () => {
            setActiveButton(sortLikesButton, sortAlphabeticalButton);
            sortByLikes(cards, cardContainer);
        });
    }

    // 초기 정렬 (sortType에 따라 정렬 실행)
    if (sortType === "alphabetical") {
        setActiveButton(sortAlphabeticalButton, sortLikesButton);
        sortAlphabetically(cards, cardContainer);
    } else if (sortType === "likes") {
        setActiveButton(sortLikesButton, sortAlphabeticalButton);
        sortByLikes(cards, cardContainer);
    }

    // 가나다순 정렬 함수
    function sortAlphabetically(cards, cardContainer) {
        const sortedCards = cards.sort((a, b) => {
            const titleA = a.querySelector(".card-title").innerText.trim();
            const titleB = b.querySelector(".card-title").innerText.trim();
            return titleA.localeCompare(titleB, "ko");
        });

        cardContainer.innerHTML = "";
        sortedCards.forEach((card) => cardContainer.appendChild(card));
    }

    // 좋아요순 정렬 함수
    function sortByLikes(cards, cardContainer) {
        const sortedCards = cards.sort((a, b) => {
            const likesA = parseInt(a.getAttribute("data-likes")) || 0;
            const likesB = parseInt(b.getAttribute("data-likes")) || 0;
            return likesB - likesA;
        });

        cardContainer.innerHTML = "";
        sortedCards.forEach((card) => cardContainer.appendChild(card));
    }

    // 버튼 활성화/비활성화 함수 (글씨 두께 변경)
    function setActiveButton(activeButton, inactiveButton) {
        // 활성화된 버튼의 글씨를 두껍게 처리
        if (activeButton) {
            activeButton.style.fontWeight = "bold"; // 글씨 두껍게
        }

        // 비활성화된 버튼의 글씨를 원래 상태로 복원
        if (inactiveButton) {
            inactiveButton.style.fontWeight = "normal"; // 글씨 원래 두께로
        }
    }
}