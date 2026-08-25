// ================================
// SHOW / HIDE PASSWORD
// ================================

const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");

const togglePassword = document.getElementById("togglePassword");
const toggleConfirm = document.getElementById("toggleConfirm");

// Password

togglePassword.addEventListener("click", function(){

    if(password.type === "password"){

        password.type = "text";

        togglePassword.classList.replace("fa-eye","fa-eye-slash");

    }else{

        password.type = "password";

        togglePassword.classList.replace("fa-eye-slash","fa-eye");

    }

});

// Confirm Password

toggleConfirm.addEventListener("click", function(){

    if(confirmPassword.type === "password"){

        confirmPassword.type = "text";

        toggleConfirm.classList.replace("fa-eye","fa-eye-slash");

    }else{

        confirmPassword.type = "password";

        toggleConfirm.classList.replace("fa-eye-slash","fa-eye");

    }

});

// ================================
// PASSWORD MATCH VALIDATION
// ================================

document.getElementById("registerForm").addEventListener("submit", function(e){

    if(password.value !== confirmPassword.value){

        e.preventDefault();

        alert("Passwords do not match!");

    }

});