document.addEventListener("submit", (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    if (form.dataset.submitted === "true") {
        e.preventDefault();
        return;
    }

    form.dataset.submitted = "true";
    const buttons = form.querySelectorAll("button[type='submit']");
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add("is-disabled");
    });
});
