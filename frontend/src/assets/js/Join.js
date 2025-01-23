// 프로필 사진 업로드 기능
const profileUpload = document.getElementById('profile-upload');
const profilePreview = document.getElementById('profile-preview');
const profileLabel = document.getElementById('profile-label');

// 파일 선택 시 미리보기 표시 및 라벨 숨기기
profileUpload.addEventListener('change', function () {
    const file = this.files[0]; // 선택한 파일 가져오기
    if (file) {
        const reader = new FileReader(); // 파일 읽기 객체 생성
        reader.onload = function (e) {
            profilePreview.src = e.target.result; // 미리보기 이미지 설정
            profilePreview.style.display = 'block'; // 미리보기 표시
            profileLabel.style.display = 'none'; // 라벨 숨기기
        };
        reader.readAsDataURL(file); // 파일을 데이터 URL로 읽기
    }
});

// 미리보기를 클릭하면 파일 선택 창 열기
profilePreview.addEventListener('click', function () {
    profileUpload.click(); // 숨겨진 input[type="file"] 요소 강제 클릭
});

