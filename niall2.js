const inputValue = document.getElementById("input");
const messagesContainer = document.getElementById("messages");

document.addEventListener("DOMContentLoaded", () => {
  inputValue.addEventListener("keydown", (e) => {
    if (e.code === "Enter") {
      let input = inputValue.value;
      inputValue.value = "";
      process(input);
    }
  });
});

function process(input)
{
  input = input.trim();

  const div = document.createElement("div")
  div.classList.add("message")
  div.classList.add("from-user")
  div.innerText = input;
  messagesContainer.appendChild(div);
}
