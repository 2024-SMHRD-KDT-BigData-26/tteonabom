// 쇼핑 데이터 가져오기 (API 요청 또는 더미 데이터)
export async function fetchShoppingData() {
    try {
        const response = await fetch('/api/shopping'); 
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("쇼핑 데이터를 불러오는 중 오류 발생:", error);
        return [];
    }
}

// 정렬 함수 (Svelte에서 호출)
export function sortShopItems(items, sortType) {
    if (sortType === "alphabetical") {
        return [...items].sort((a, b) => a.title.localeCompare(b.title, "ko"));
    } else if (sortType === "likes") {
        return [...items].sort((a, b) => b.likes - a.likes);
    }
    return items;
}

// 샘플 쇼핑몰 데이터
export const shopItems = [
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크A",
      likes: 15,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle01.png",
      category: "#자전거",
      title: "바이크B",
      likes: 20,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크C",
      likes: 10,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크D",
      likes: 25,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크E",
      likes: 5,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크F",
      likes: 30,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크G",
      likes: 18,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크H",
      likes: 22,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
      img: "/src/assets/img/bicycle00.png",
      category: "#자전거",
      title: "바이크I",
      likes: 14,
      url: "http://shop1.jaike.cafe24.com/",
    },
    {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      },
      {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      },
      {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      },
      {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      },
      {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      },
      {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      },
      {
        img: "/src/assets/img/bicycle00.png",
        category: "#자전거",
        title: "바이크I",
        likes: 14,
        url: "http://shop1.jaike.cafe24.com/",
      }
];
