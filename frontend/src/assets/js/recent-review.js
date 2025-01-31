import { writable } from 'svelte/store';
import { recentReviews } from './recent-review-data.js';

export const displayedReviews = writable(recentReviews.slice(0, 6)); // 초기 6개 이미지 표시
export const loading = writable(false);  // 데이터 로딩 상태 추적

export const loadMoreReviews = (entries, observer) => {
  if (entries[0].isIntersecting) {
    loading.set(true); // 로딩 시작

    setTimeout(() => {
      displayedReviews.update((currentReviews) => {
        const nextIndex = currentReviews.length;
        const newReviews = recentReviews.slice(nextIndex, nextIndex + 6); // 다음 6개 로드
        return [...currentReviews, ...newReviews];
      });

      loading.set(false); // 로딩 종료
    }, 1000); // 1초 딜레이 (테스트용)
  }
};