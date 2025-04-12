document.getElementById("send-command").addEventListener("click", () => {
    const commandInput = document.getElementById("command-input");
    const command = commandInput.value.trim().toLowerCase();
    const responseOutput = document.getElementById("response-output");

    if (!command) {
        responseOutput.textContent = "Please enter a command.";
        return;
    }

    // Send the command to the Flask server
    fetch("http://127.0.0.1:5000/command", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ command })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            responseOutput.textContent = data.response;
        })
        .catch(error => {
            responseOutput.textContent = `Error: ${error.message}`;
        });
});