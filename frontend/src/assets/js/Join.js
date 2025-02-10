import { tick } from "svelte";

export let isIdAvailable = null;
export let isNickAvailable = null;

// 유효성 검사 함수
export function validateForm(userId, password, confirmPassword, nickname) {
  let idError = "";
  let passwordError = "";
  let nickError = "";
  let isValid = true;

  // 아이디: 5~10자 (영문 소문자와 숫자)
  if (!userId || userId.trim().length < 5 || userId.trim().length > 10) {
    idError = "아이디는 5~10자 사이여야 합니다.";
    isValid = false;
  }

  // 비밀번호: 8~16자, 영문 대문자, 소문자, 숫자 포함
  if (!password || password.length < 8 || password.length > 16) {
    passwordError = "비밀번호는 8~16자여야 합니다.";
    isValid = false;
  } else {
    const uppercasePattern = /[A-Z]/;
    const lowercasePattern = /[a-z]/;
    const digitPattern = /\d/;
    if (!uppercasePattern.test(password) || !lowercasePattern.test(password) || !digitPattern.test(password)) {
      passwordError = "비밀번호는 대문자, 소문자, 숫자를 포함해야 합니다.";
      isValid = false;
    }
  }

  // 비밀번호 일치 확인
  if (password !== confirmPassword) {
    passwordError = "비밀번호가 일치하지 않습니다.";
    isValid = false;
  }

  // 닉네임: 1~8자
  if (!nickname || nickname.trim().length < 1 || nickname.trim().length > 8) {
    nickError = "닉네임은 1~8자 사이여야 합니다.";
    isValid = false;
  }

  return { isValid, idError, passwordError, nickError };
}

// 회원가입 폼 제출 핸들러 (단일 정의)
export function handleSubmit(
  event,
  userId,
  password,
  confirmPassword,
  nickname,
  profileImage,
  setErrors,
  submitToBackend
) {
  event.preventDefault();

  // 기본 유효성 검사 수행
  const { isValid, idError, passwordError, nickError } = validateForm(
    userId,
    password,
    confirmPassword,
    nickname
  );
  setErrors({ idError, passwordError, nickError });

  // 중복 검사 여부 확인
  if (isIdAvailable !== true) {
    alert("아이디 중복 검사를 진행해주세요.");
    return;
  }
  if (isNickAvailable !== true) {
    alert("닉네임 중복 검사를 진행해주세요.");
    return;
  }

  // 유효성 검사가 통과되면 회원가입 요청 진행
  if (isValid) {
    submitToBackend({ userId, password, nickname, profileImage });
  }
}

// ✅ 아이디 중복 확인 함수
export async function checkUserId(userId, setErrors) {
  if (!userId.trim()) {
    setErrors((prev) => ({ ...prev, idError: "아이디를 입력하세요." }));
    alert("🚨 아이디를 입력하세요.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:9000/api/check-id?USER_ID=${encodeURIComponent(userId)}`);
    
    if (!response.ok) {
      throw new Error("서버 오류 발생");
    }

    const data = await response.json();
    isIdAvailable = data.available;

    const message = isIdAvailable ? "✅ 사용 가능한 아이디입니다." : "❌ 이미 사용 중인 아이디입니다.";
    alert(message);

    setErrors((prev) => ({
      ...prev,
      idError: message,
    }));

  } catch (error) {
    console.error("❌ 아이디 중복 확인 오류:", error);
    alert("🚨 아이디 중복 확인에 실패했습니다.");
    setErrors((prev) => ({ ...prev, idError: "아이디 중복 확인에 실패했습니다." }));
  }
}

// ✅ 닉네임 중복 확인 함수
export async function checkNickname(nickname, setErrors) {
  if (!nickname.trim()) {
    setErrors((prev) => ({ ...prev, nickError: "닉네임을 입력하세요." }));
    alert("🚨 닉네임을 입력하세요.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:9000/api/check-nick?USER_NICK=${encodeURIComponent(nickname)}`);
    
    if (!response.ok) {
      throw new Error("서버 오류 발생");
    }

    const data = await response.json();
    isNickAvailable = data.available;

    const message = isNickAvailable ? "✅ 사용 가능한 닉네임입니다." : "❌ 이미 사용 중인 닉네임입니다.";
    alert(message);

    setErrors((prev) => ({
      ...prev,
      nickError: message,
    }));

  } catch (error) {
    console.error("❌ 닉네임 중복 확인 오류:", error);
    alert("🚨 닉네임 중복 확인에 실패했습니다.");
    setErrors((prev) => ({ ...prev, nickError: "닉네임 중복 확인에 실패했습니다." }));
  }
}

// ✅ 프로필 이미지 업로드 및 미리보기 (서버 업로드 후 URL 저장)
export function handleProfileUpload(event, callback) {
  const file = event.target.files[0];

  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      alert("이미지 크기는 2MB를 초과할 수 없습니다.");
      return;
    }

    const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
    if (!allowedTypes.includes(file.type)) {
      alert("jpg, png, gif 형식의 이미지만 업로드 가능합니다.");
      return;
    }

    const reader = new FileReader();
    reader.onload = async (e) => {
      callback(e.target.result, file);
    };

    reader.readAsDataURL(file);
  }
}

// ✅ 프로필 이미지 서버 업로드 (백엔드 9000 포트 사용)
export async function uploadProfileImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:9000/api/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("파일 업로드 실패");
    }

    const data = await response.json();
    return `http://127.0.0.1:9000${data.fileUrl}`;
  } catch (error) {
    console.error("❌ 프로필 이미지 업로드 오류:", error);
    return "";
  }
}

// ✅ 파일 업로드 창 열기 함수
export function openFileDialog(profileUpload) {
  if (profileUpload) {
    profileUpload.click();
  
}
}
