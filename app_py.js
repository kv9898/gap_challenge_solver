// Handler for Keys
$(document).on("keyup", function (event) {
  if (event.key == "Enter") {
    Shiny.setInputValue("key", event.key, { priority: "event" });
  } else if (event.key == "`") {
    Shiny.setInputValue("key", event.key, { priority: "event" });
  } else {
    Shiny.setInputValue("key", "");
  }
});

// Paste event listener to handle image pasting
$(document).on("paste", function (event) {
  const clipboardData = event.originalEvent.clipboardData || window.clipboardData;
  if (clipboardData && clipboardData.items) {
    // Loop through clipboard items to find an image
    for (let i = 0; i < clipboardData.items.length; i++) {
      const item = clipboardData.items[i];
      if (item.type.startsWith("image")) {
        const file = item.getAsFile();
        const reader = new FileReader();
        
        reader.onload = function (e) {
          // Send the base64 image data to the Shiny server
          Shiny.setInputValue("paste_image", e.target.result, { priority: "event" });
        };
        
        reader.readAsDataURL(file);  // Read image as base64 data URL
        break;
      }
    }
  }
});

// Drag-and-drop event listeners for handling image drop
$(document).on("dragover", function (event) {
  event.preventDefault();
  event.stopPropagation();
  $(this).css("background-color", "#e0e0e0"); // Optional: highlight the drop area
});

$(document).on("dragleave", function (event) {
  event.preventDefault();
  event.stopPropagation();
  $(this).css("background-color", ""); // Reset background color
});

$(document).on("drop", function (event) {
  event.preventDefault();
  event.stopPropagation();
  $(this).css("background-color", ""); // Reset background color

  const dt = event.originalEvent.dataTransfer;
  if (dt && dt.files.length > 0) {
    const file = dt.files[0];
    if (file.type.startsWith("image")) {
      const reader = new FileReader();
      
      reader.onload = function (e) {
        // Send the base64 image data to the Shiny server
        Shiny.setInputValue("paste_image", e.target.result, { priority: "event" });
      };
      
      reader.readAsDataURL(file);  // Read image as base64 data URL
    }
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
