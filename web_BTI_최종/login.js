// 로그인폼
const loginForm = document.getElementById("login-form");
loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    // 실제 서버로 요청을 보내는 부분은 여기에 추가
    // 예시로 입력된 값을 alert으로 보여줍니다.
    
    alert(`Username: ${username}, Password: ${password}`);
});

// 회원가입
const signupButton = document.querySelector(".signup-button");
signupButton.addEventListener('click', function() {
    window.location.href = 'register.html';
});

// 아이디 비밀번호 찾기
const forgotText = document.querySelector(".forgot-text");
forgotText.addEventListener("click", () => {
    // 아이디, 비밀번호 찾기 기능을 수행하는 로직을 여기에 추가합니다.
    // 예시로 메시지를 띄우는 기능을 추가합니다.
    alert("아이디와 비밀번호 찾기 기능은 구현되지 않았습니다.");
});