// // 입력 폼 유효성 검사 함수
// export function validateForm(userId, password, confirmPassword, nickname) {
//     let idError = '';
//     let passwordError = '';
//     let nickError = '';
  
//     // 아이디 검증: 5~10자의 영문 소문자와 숫자
//     if (!/^[a-z0-9]{5,10}$/.test(userId)) {
//       idError = '아이디는 5~10자 사이의 영문 소문자와 숫자여야 합니다.';
//     }

//     // 비밀번호 일치 검증
//     if (password !== confirmPassword) {
//       passwordError = '비밀번호가 일치하지 않습니다.';
//     }

//     // 비밀번호 강도 검증 추가: 8~16자, 대소문자, 숫자 포함
//     if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/.test(password)) {
//       passwordError = '비밀번호는 8~16자의 대소문자, 숫자를 포함해야 합니다.';
//     }

//     // 닉네임 검증: 1~8자
//     if (nickname.length < 1 || nickname.length > 8) {
//       nickError = '닉네임은 1~8자 사이여야 합니다.';
//     }
  
//     // 모든 검증 결과 반환
//     return { 
//       isValid: !idError && !passwordError && !nickError, 
//       idError, 
//       passwordError, 
//       nickError 
//     };
//   }

// 프로필 이미지 업로드 및 미리보기 함수
export function handleProfileUpload(event, setProfilePreview) {
    const file = event.target.files[0];
    if (file) {
      // 이미지 파일 크기 제한 (2MB)
      if (file.size > 2 * 1024 * 1024) {
        alert('이미지 크기는 2MB를 초과할 수 없습니다.');
        return;
      }

      // 허용된 이미지 타입 확인
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        alert('jpg, png, gif 형식의 이미지만 업로드 가능합니다.');
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        setProfilePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }

// 숨겨진 파일 입력 요소 클릭 함수  
export function openFileDialog(profileUpload) {
    profileUpload.click();
  }

// 폼 제출 핸들러  
export function handleSubmit(event, userId, password, confirmPassword, nickname, setErrors, submitToBackend) {
    event.preventDefault();
  
    // 폼 유효성 검사
    const { isValid, idError, passwordError, nickError } = validateForm(userId, password, confirmPassword, nickname);
  
    // 에러 상태 업데이트
    // setErrors({ idError, passwordError, nickError });
  
    // 모든 입력값이 유효한 경우
    if (isValid) {
      // 백엔드 제출 함수 호출
      submitToBackend({ userId, password, nickname });
    }
  }