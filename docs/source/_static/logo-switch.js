function isDarkTheme() {
    const theme = document.body.dataset.theme;

    if (theme === "dark") {
        return true;
    }

    if (theme === "light") {
        return false;
    }

    // theme === "auto"
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function updateLogo() {
    const dark = isDarkTheme();

    const pageLogo = document.getElementById("pyr4t-logo");
    if (pageLogo) {
        pageLogo.src = dark
            ? "_static/logo-dark.png"
            : "_static/logo-light.png";
    }

    const sidebarLogo = document.querySelector(".sidebar-brand img");
    if (sidebarLogo) {
        sidebarLogo.src = dark
            ? "_static/logo-dark.png"
            : "_static/logo-light.png";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    updateLogo();

    new MutationObserver(updateLogo).observe(
        document.body,
        {
            attributes: true,
            attributeFilter: ["data-theme"],
        },
    );
});
