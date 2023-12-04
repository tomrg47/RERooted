document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");
  const loginToggle = document.getElementById("loginToggle");
  const signupToggle = document.getElementById("signupToggle");

  loginToggle.addEventListener("change", function () {
    if (loginToggle.checked) {
      loginForm.style.display = "block";
      signupForm.style.display = "none";
    }
  });

  signupToggle.addEventListener("change", function () {
    if (signupToggle.checked) {
      loginForm.style.display = "none";
      signupForm.style.display = "block";
    }
  });
});
