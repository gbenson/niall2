const theInput = document.getElementById("input");
const messages = document.getElementById("messages");

document.addEventListener("DOMContentLoaded", () => {
  theInput.addEventListener("keydown", (e) => {
    if (e.code === "Enter") {
      let userInput = theInput.value;
      theInput.value = "";
      processInput(userInput);
    }
  });
});

function processInput(userInput) {
  userInput = userInput.trim();
  addToChat("user", userInput);

  const niallDiv = addToChat("niall", "...");
  niallDiv.innerText = "hello from niall"
}

function addToChat(sender, message) {
  const div = document.createElement("div");
  div.classList.add("message");
  div.classList.add(`from-${sender}`);
  div.innerText = message;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight - messages.clientHeight;
  return div;
}
