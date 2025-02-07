import { tick } from "svelte";

export let isIdAvailable = null;
export let isNickAvailable = null;
// ✅ 폼 제출 핸들러 (회원가입 요청) 
export function handleSubmit(event, userId, password, confirmPassword, nickname, profileImage, setErrors, submitToBackend) {
  event.preventDefault();

  const { isValid, idError, passwordError, nickError } = validateForm(userId, password, confirmPassword, nickname);
  setErrors({ idError, passwordError, nickError });

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
    alert(message);  // ✅ 결과를 alert 창으로 띄우기

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
    alert(message);  // ✅ 결과를 alert 창으로 띄우기

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
      callback(e.target.result, file); // ✅ file도 함께 전달
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
    return `http://127.0.0.1:9000${data.fileUrl}`;  // ✅ 9000 포트 사용

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
