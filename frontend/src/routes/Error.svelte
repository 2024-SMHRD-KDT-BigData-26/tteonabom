<script>
    function goHome() {
        window.location.href = "/";
    }
</script>

<div class="error-container">
    <img src="/src/assets/img/Logo.png" alt="Logo" class="logo_img" />
    <img src="/src/assets/img/error_img.png" alt="error" class="error_img">
    <p class ="error_text">
        요청하신 페이지를 찾을 수 없습니다. <br /> 홈페이지 이용에 불편을 드려 죄송합니다.
    </p>
    <button class="btn" on:click={goHome}>메인으로 돌아가기</button>
</div>

<style>
    .error-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    .logo_img {
        width: 400px;
    }
    .error_img {
        padding: 20px;
        width: 200px;
    }
    .error_text {
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .btn {
        background-color: #444444;
        background-color: #444;
        color: white;
        padding: 12px 80px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
</style>
