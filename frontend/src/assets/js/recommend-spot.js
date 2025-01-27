// recommend-spot.js
export class RecommendSpotCarousel {
    constructor(spots) {
      this.spots = spots;
      this.currentIndex = 0;
    }
  
    // 현재 인덱스로부터 3개의 항목을 가져오는 메서드
    getDisplayedSpots() {
      return [
        this.spots[(this.currentIndex) % this.spots.length],
        this.spots[(this.currentIndex + 1) % this.spots.length],
        this.spots[(this.currentIndex + 2) % this.spots.length]
      ];
    }
  
    // 왼쪽 이동 버튼
    prevItem() {
      this.currentIndex = (this.currentIndex - 1 + this.spots.length) % this.spots.length;
      return this.getDisplayedSpots();
    }
  
    // 오른쪽 이동 버튼
    nextItem() {
      this.currentIndex = (this.currentIndex + 1) % this.spots.length;
      return this.getDisplayedSpots();
    }
  }