document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const inputs = form.querySelectorAll("input[required]");
            let valid = true;
            inputs.forEach(function (input) {
                input.classList.remove("input-error");
                if (input.value.trim() === "") {
                    valid = false;
                    input.classList.add("input-error");
                }
            });
            if (!valid) {
                event.preventDefault();
                showNotification("Please fill in all required fields.", "error");
            }
        });
    });
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    phoneInputs.forEach(function (input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9+ ]/g, "");
        });
    });
    const deleteButtons = document.querySelectorAll(".delete-button");
    deleteButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            const confirmed = confirm(
                "Are you sure you want to delete this contact?"
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    const searchInput = document.querySelector(
        '.search input[name="search"]'
    );
    if (searchInput) {
        searchInput.addEventListener(
            "focus",
            function () {
                this.classList.add("search-focus");
            }
        );
        searchInput.addEventListener(
            "blur",
            function () {
                this.classList.remove("search-focus");
            }
        );
    }
    const tableRows = document.querySelectorAll(
        ".contacts table tr"
    );
    tableRows.forEach(function (row, index) {
        if (index > 0) {
            row.style.opacity = "0";
            row.style.transform = "translateY(10px)";
            setTimeout(function () {
                row.style.transition = "all 0.3s ease";
                row.style.opacity = "1";
                row.style.transform = "translateY(0)";
            }, index * 80);
        }
    });
    const message = document.querySelector(".message");
    if (message) {
        setTimeout(function () {
            message.style.transition = "opacity 0.5s ease";
            message.style.opacity = "0";
        }, 4000);
    }
    window.showNotification = function (
        text,
        type = "success"
    ) {
        const oldNotification =
            document.querySelector(".js-notification");
        if (oldNotification) {
            oldNotification.remove();
        }
        const notification =
            document.createElement("div");
        notification.className =
            "js-notification " + type;
        notification.textContent = text;
        document.body.appendChild(
            notification
        );
        setTimeout(function () {
            notification.classList.add("show");
        }, 10);
        setTimeout(function () {
            notification.classList.remove("show");
            setTimeout(function () {
                notification.remove();
            }, 500);
        }, 3500);
    };
    const backToTop =
        document.createElement("button");
    backToTop.className =
        "back-to-top";
    backToTop.textContent = "↑";
    document.body.appendChild(
        backToTop
    );
    window.addEventListener(
        "scroll",
        function () {
            if (window.scrollY > 300) {
                backToTop.classList.add("show");
            } else {
                backToTop.classList.remove("show");
            }
        }
    );
    backToTop.addEventListener(
        "click",
        function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    );
    forms.forEach(function (form) {
        form.addEventListener(
            "submit",
            function () {
                const submitButton =
                    form.querySelector(
                        'button[type="submit"]'
                    );
                if (submitButton) {
                    setTimeout(function () {
                        submitButton.disabled = true;
                        submitButton.textContent =
                            "Please wait...";
                    }, 50);
                }
            }
        );
    });
});
function togglePassword() {
    const password =
        document.getElementById("password");
    const eye =
        document.getElementById("password-eye");
    if (password.type === "password") {
        password.type = "text";
        eye.textContent = "🙈";
    } else {
        password.type = "password";
        eye.textContent = "👁️";
    }
}
function toggleSignupPassword() {
    const password = document.getElementById("signup-password");
    const eye = document.getElementById("signup-password-eye");
    if (password.type === "password")
         {password.type = "text";
          eye.textContent = "🙈";}
    else {
        password.type = "password";
        eye.textContent = "👁️";}
}
function toggleAccountPassword(passwordId, eyeId) {
    const password = document.getElementById(passwordId);
    const eye = document.getElementById(eyeId);
    if (password.type === "password") {
        password.type = "text";
        eye.textContent = "🙈";} 
    else {
        password.type = "password";
        eye.textContent = "👁️";}
}
function toggleMenu(){
const menu=document.getElementById("mobileMenu");
menu.classList.toggle("show-menu");
}