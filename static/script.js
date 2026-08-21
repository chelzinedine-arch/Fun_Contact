function toggleMenu() {
    const mobileMenu = document.getElementById("mobileMenu");
    if (mobileMenu) {mobileMenu.classList.toggle("show-menu");}}
document.addEventListener("DOMContentLoaded", function () {
    const mobileLinks = document.querySelectorAll("#mobileMenu a");
    mobileLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            const mobileMenu = document.getElementById("mobileMenu");
            if (mobileMenu) { mobileMenu.classList.remove("show-menu");}});});
    const backToTop = document.querySelector(".back-to-top");
    if (backToTop) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 300) {
                backToTop.classList.add("show");}
            else {
                backToTop.classList.remove("show");}});
        backToTop.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth"});});}
    const passwordInputs = document.querySelectorAll( 'input[type="password"]');
    passwordInputs.forEach(function (input) {
        input.addEventListener("input", function () {
            if (input.value.length > 0) {
                input.classList.add("input-success");}
            else {
                input.classList.remove("input-success");}});});
    const searchInputs = document.querySelectorAll( '.search input');
    searchInputs.forEach(function (input) {
        input.addEventListener("focus", function () {input.classList.add("search-focus");});
        input.addEventListener("blur", function () { input.classList.remove("search-focus");});});
    const forms = document.querySelectorAll("form");
    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const submitButton = form.querySelector( 'button[type="submit"]');
            if (submitButton) {
                submitButton.classList.add("loading");
                submitButton.disabled = true;
                setTimeout(function () {
                    submitButton.disabled = false;
                    submitButton.classList.remove("loading");}, 3000);}});});
    const notification = document.querySelector(".js-notification");
    if (notification) {
        setTimeout(function () {
            notification.classList.add("show");}, 100);
        setTimeout(function () {
            notification.classList.remove("show");}, 4000);}
    const deleteForms = document.querySelectorAll( 'form[action*="/delete/"]');
    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm(
                "Are you sure you want to delete this contact?");
            if (!confirmed) { event.preventDefault();}});});
    const passwordBoxes = document.querySelectorAll(".password-box");
    passwordBoxes.forEach(function (box) {
        const input = box.querySelector("input");
        const eye = box.querySelector(".password-eye");
        if (input && eye) {
            eye.addEventListener("click", function () {
                if (input.type === "password") {
                    input.type = "text";
                    eye.textContent = "🙈";}
                else {
                    input.type = "password";
                    eye.textContent = "👁";}});}});
    const confirmPassword = document.querySelector( 'input[name="confirm_password"]');
    const newPassword = document.querySelector('input[name="new_password"]');
    if (confirmPassword && newPassword) {
        confirmPassword.addEventListener("input", function () {
            if (confirmPassword.value !== newPassword.value && confirmPassword.value.length > 0)
             {confirmPassword.classList.add("input-error");confirmPassword.classList.remove("input-success");} 
            else if (confirmPassword.value === newPassword.value && confirmPassword.value.length > 0)
             { confirmPassword.classList.remove("input-error"); confirmPassword.classList.add("input-success");}
            else {confirmPassword.classList.remove("input-error");confirmPassword.classList.remove("input-success");}});}
    const resetButtons = document.querySelectorAll('button[type="reset"]');
    resetButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const form = button.closest("form");
            if (form) {
                setTimeout(function () {
                    const inputs = form.querySelectorAll("input");
                    inputs.forEach(function (input) {
                        input.classList.remove("input-error");
                        input.classList.remove("input-success");});}, 50);}});});
    const animatedElements = document.querySelectorAll( ".fade-in, .slide-left, .slide-right, .zoom-in");
    animatedElements.forEach(function (element) { element.style.animationPlayState = "running";});});
window.addEventListener("resize", function () {
    const mobileMenu = document.getElementById("mobileMenu");
    if (window.innerWidth > 900 && mobileMenu) { mobileMenu.classList.remove("show-menu");}});