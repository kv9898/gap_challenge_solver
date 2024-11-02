$(document).on("keyup", function (event) {
  if (event.key == "Enter") {
    Shiny.setInputValue("key", event.key, { priority: "event" });
    console.log(event.key);
  } else if (event.key == "`") {
    console.log(event.key);
    Shiny.setInputValue("key", event.key, { priority: "event" });
  } else {
    Shiny.setInputValue("key", "");
  }
});
// colour mode
window.addEventListener(
  "message",
  function (e) {
    // Check the origin of the sender
    if (e.data === "light-mode") {
      document.documentElement.dataset.bsTheme = "light";
      document.documentElement.style.setProperty("--bs-body-bg", "#f9fffe");
    } else if (e.data === "dark-mode") {
      document.documentElement.dataset.bsTheme = "dark";
      document.documentElement.style.setProperty("--bs-body-bg", "#16242f");
    }
  },
  false
);

window.parent.postMessage("ShinyColorQuery", "*");
