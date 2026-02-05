const rows = document.querySelectorAll("[data-swipe]");

rows.forEach((row) => {
    let startX = 0;
    let startY = 0;
    let currentX = 0;
    let currentY = 0;
    let isDragging = false;
    let isLocked = false;
    let moved = false;
    let pointerType = "touch";

    const card = row.querySelector(".swipe-card");
    const maxTranslate = 72;
    const openThreshold = -35;
    const lockThreshold = 8;

    function setTranslate(x) {
        const clamped = Math.max(-maxTranslate, Math.min(0, x));
        card.style.transform = `translateX(${clamped}px)`;
    }

    function onStart(x, y) {
        startX = x;
        startY = y;
        currentX = x;
        currentY = y;
        isDragging = true;
        isLocked = false;
        moved = false;
    }

    function onMove(x, y, e) {
        if (!isDragging) return;
        currentX = x;
        currentY = y;
        const dx = currentX - startX;
        const dy = currentY - startY;
        if (!isLocked) {
            if (Math.abs(dx) > lockThreshold || Math.abs(dy) > lockThreshold) {
                isLocked = Math.abs(dx) > Math.abs(dy);
            } else {
                return;
            }
        }
        if (isLocked) {
            if (pointerType !== "mouse") {
                e.preventDefault();
            }
            moved = true;
            setTranslate(dx);
        }
    }

    function onEnd() {
        if (!isDragging) return;
        isDragging = false;
        if (!moved) return;
        const dx = currentX - startX;
        if (dx < openThreshold) {
            card.style.transform = `translateX(-${maxTranslate}px)`;
            row.classList.add("open");
        } else {
            card.style.transform = "";
            row.classList.remove("open");
        }
    }

    row.addEventListener(
        "touchstart",
        (e) => {
            pointerType = "touch";
            onStart(e.touches[0].clientX, e.touches[0].clientY);
        },
        { passive: true }
    );
    row.addEventListener(
        "touchmove",
        (e) => onMove(e.touches[0].clientX, e.touches[0].clientY, e),
        { passive: false }
    );
    row.addEventListener("touchend", onEnd);

    row.addEventListener("pointerdown", (e) => {
        if (e.pointerType === "mouse" && e.button !== 0) return;
        pointerType = e.pointerType || "mouse";
        if (pointerType !== "mouse") {
            row.setPointerCapture(e.pointerId);
        }
        onStart(e.clientX, e.clientY);
    });
    row.addEventListener("pointermove", (e) => onMove(e.clientX, e.clientY, e));
    row.addEventListener("pointerup", onEnd);
    row.addEventListener("pointercancel", onEnd);

    row.addEventListener(
        "wheel",
        (e) => {
            if (Math.abs(e.deltaX) < 15) return;
            if (e.deltaX > 0) {
                card.style.transform = `translateX(-${maxTranslate}px)`;
                row.classList.add("open");
            } else {
                card.style.transform = "";
                row.classList.remove("open");
            }
        },
        { passive: true }
    );
});
