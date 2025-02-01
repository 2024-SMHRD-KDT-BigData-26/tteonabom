// 시간 변환 함수
export function timeAgo(date) {
    const now = new Date();
    const past = new Date(date);
    const diffInSeconds = Math.floor((now - past) / 1000);
    
    const timeIntervals = [
        { label: "년", seconds: 31536000 },
        { label: "개월", seconds: 2592000 },
        { label: "일", seconds: 86400 },
        { label: "시간", seconds: 3600 },
        { label: "분", seconds: 60 },
        { label: "초", seconds: 1 }
    ];

    for (const interval of timeIntervals) {
        const diff = Math.floor(diffInSeconds / interval.seconds);
        if (diff >= 1) {
            return `${diff} ${interval.label} 전`;
        }
    }
    
    return "방금 전";
}
