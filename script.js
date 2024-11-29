const toggleButton = document.getElementById("toggle-dark-mode");

toggleButton.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("default");
});

function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'pt-BR'; // Define o idioma
    window.speechSynthesis.speak(speech);
  }