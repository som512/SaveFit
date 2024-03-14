const showPasswordButton = document.getElementById("hidden_button");
showPasswordButton.addEventListener("click", togglePasswordVisibility);

const header_right = document.getElementById('header2-right1');
header_right.addEventListener('mouseover', function(){
  const dropdown_menu = document.getElementById('dropdown-nav')
  dropdown_menu.style.visibility = "visible";
});


function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    showPasswordButton.value = "非表示";
  } else {
    passwordInput.type = "password";
    showPasswordButton.value = "表示";
  }
}

