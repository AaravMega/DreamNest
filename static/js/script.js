document.addEventListener("DOMContentLoaded", function () {
    // Mobile nav toggle
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("navLinks");
    if (hamburger && navLinks) {
        hamburger.addEventListener("click", function () {
            navLinks.classList.toggle("open");
        });
    }

    // FAQ accordion
    const faqItems = document.querySelectorAll(".faq-item");
    faqItems.forEach(function (item) {
        const question = item.querySelector(".faq-question");
        question.addEventListener("click", function () {
            const isActive = item.classList.contains("active");
            faqItems.forEach(function (i) { i.classList.remove("active"); });
            if (!isActive) {
                item.classList.add("active");
            }
        });
    });

    // Auto-dismiss flash messages
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.transition = "opacity 0.4s ease";
            flash.style.opacity = "0";
            setTimeout(function () { flash.remove(); }, 400);
        }, 4000);
    });
});
