$(document).ready(() => {
  const $themeToggle = $("#theme-toggle");
  const savedTheme = localStorage.getItem("theme") || "light";
  $("html").attr("data-theme", savedTheme);

  updateThemeToggleUI(savedTheme);

  $themeToggle.on("click", function () {
    const currentTheme = $("html").attr("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";

    $("html").attr("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeToggleUI(newTheme);
  });
});

function updateThemeToggleUI(theme) {
  const $themeToggle = $("#theme-toggle");
  const $icon = $themeToggle.find("i");
  const $text = $themeToggle.find("span");

  if (theme === "light") {
    $icon.attr("class", "fas fa-sun");
    $text.text("Light Mode");
  } else {
    $icon.attr("class", "fas fa-moon");
    $text.text("Dark Mode");
  }
}
