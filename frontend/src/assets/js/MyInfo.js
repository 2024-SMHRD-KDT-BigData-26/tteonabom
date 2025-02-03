// 내 정보 변경 폼 유효성 검사 함수
// MyInfo.js
export function validateForm(currentPassword, newPassword, confirmNewPassword, nickname) {
    let passwordError = '';
    let nickError = '';
  
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/.test(currentPassword)) {
      passwordError = '기존 비밀번호가 올바르지 않습니다. (8~16자의 대소문자, 숫자 포함)';
    }
  
    if (newPassword !== confirmNewPassword) {
      passwordError = '새 비밀번호가 일치하지 않습니다.';
    }
  
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/.test(newPassword)) {
      passwordError = '새 비밀번호는 8~16자의 대소문자, 숫자를 포함해야 합니다.';
    }
  
    if (nickname.length < 1 || nickname.length > 8) {
      nickError = '닉네임은 1~8자 사이여야 합니다.';
    }
  
    return {
      isValid: !passwordError && !nickError,
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
  export function handleSubmit(event, currentPassword, newPassword, confirmNewPassword, nickname, setErrors, submitToBackend) {
    event.preventDefault();
    const { isValid, passwordError, nickError } = validateForm(currentPassword, newPassword, confirmNewPassword, nickname);
    setErrors({ passwordError, nickError });
  
    if (isValid) {
        submitToBackend({ currentPassword, newPassword, nickname });
    }
  }

  // 닉네임 중복확인
export async function checkNickname(nickname, setErrors) {
  try {
    const response = await fetch('http://localhost:9000/api/check-nickname', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nickname })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || '닉네임 중복 확인 중 오류가 발생했습니다.');
    }

    if (data.isDuplicate) {
      setErrors({ nickError: '이미 사용 중인 닉네임입니다.' });
    } else {
      setErrors({ nickError: '' });
      alert('사용 가능한 닉네임입니다.');
    }
  } catch (error) {
    console.error('❌ 닉네임 중복 확인 실패:', error);
    setErrors({ nickError: error.message });
  }
}
  