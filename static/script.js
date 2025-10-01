const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("fileInput");
const uploadForm = document.getElementById("uploadForm");
const previewSection = document.getElementById("previewSection");

// click opens file dialog
dropArea.addEventListener("click", () => fileInput.click());

// drag & drop UI
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.classList.add("hover");
});
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("hover");
});
dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.classList.remove("hover");
  if (e.dataTransfer.files.length) {
    fileInput.files = e.dataTransfer.files;
  }
});

// show temp message on submit — server renders actual preview
uploadForm.addEventListener("submit", () => {
  previewSection.innerHTML = "<p class='placeholder'>Generating preview... please wait</p>";
});
