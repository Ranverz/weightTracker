const tg = window.Telegram?.WebApp;
if (!tg) {
    console.warn("Telegram WebApp SDK not found");
} else {
    tg.ready();
    tg.expand();
}

if (tg?.initData) {
    fetch("/miniapp/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ initData: tg.initData }),
    })
        .then((resp) => {
            if (!resp.ok) return;
            const marker = "tg_auth_done";
            if (!sessionStorage.getItem(marker)) {
                sessionStorage.setItem(marker, "1");
                window.location.reload();
            }
        })
        .catch(() => {});
}
