// 입력 폼 유효성 검사 함수
export function validateForm(userId, password, confirmPassword, nickname) {
  let idError = '';
  let passwordError = '';
  let nickError = '';

  if (!/^[a-z0-9]{5,10}$/.test(userId)) {
    idError = '아이디는 5~10자 사이의 영문 소문자와 숫자여야 합니다.';
  }

  if (password !== confirmPassword) {
    passwordError = '비밀번호가 일치하지 않습니다.';
  }

  if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/.test(password)) {
    passwordError = '비밀번호는 8~16자의 대소문자, 숫자를 포함해야 합니다.';
  }

  if (nickname.length < 1 || nickname.length > 8) {
    nickError = '닉네임은 1~8자 사이여야 합니다.';
  }

  return {
    isValid: !idError && !passwordError && !nickError,
    idError,
    passwordError,
    nickError,
  };
}

// 프로필 이미지 업로드 및 미리보기 함수
export function handleProfileUpload(event, setProfilePreview) {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      alert('이미지 크기는 2MB를 초과할 수 없습니다.');
      return;
    }
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

// 파일 업로드 창 열기
export function openFileDialog(profileUpload) {
  profileUpload.click();
}

// 폼 제출 핸들러  
export function handleSubmit(event, userId, password, confirmPassword, nickname, setErrors, submitToBackend) {
  event.preventDefault();
  const { isValid, idError, passwordError, nickError } = validateForm(userId, password, confirmPassword, nickname);
  setErrors({ idError, passwordError, nickError });

  if (isValid) {
      submitToBackend({ userId, password, nickname });
  }
}
