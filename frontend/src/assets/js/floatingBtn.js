import { writable } from 'svelte/store';

export const isVisible = writable(false); // 버튼의 표시 여부를 writable store로 관리

// 스크롤 이벤트 핸들러
export const handleScroll = () => {
    const scrollPosition = window.scrollY; // 현재 스크롤 위치
    const windowHeight = window.innerHeight; // 현재 창의 높이
    const docHeight = document.documentElement.scrollHeight; // 전체 문서의 높이
  
    // 화면의 스크롤 위치가 100px 이상이면 버튼을 표시하고
    // 페이지의 끝에서 50px 이내로 가면 버튼을 숨김
    if (scrollPosition > 100 && scrollPosition < docHeight - windowHeight - 50) {
      isVisible.set(true); // 버튼을 표시
    } else {
      isVisible.set(false); // 버튼을 숨김
    }
  };

// 최상단으로 스크롤 이동
export const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// 컴포넌트가 마운트될 때 스크롤 이벤트를 등록하고, 언마운트될 때 해제
export function floatingBtnActions(node) {
  window.addEventListener("scroll", handleScroll);

  return {
    destroy: () => {
      window.removeEventListener("scroll", handleScroll);
    }
  };
}
