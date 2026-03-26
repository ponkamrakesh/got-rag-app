async function send() {
  const input = document.getElementById("input").value;
  const res = await fetch("/chat?q=" + input, { method: "POST" });
  const data = await res.json();
  document.getElementById("chat").innerHTML += input + " -> " + data.response + "\n";
}