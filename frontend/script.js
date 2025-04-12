// Ensure DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
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

    // Handle command button clicks
    document.querySelectorAll(".command-button").forEach(button => {
        button.addEventListener("click", () => {
            const command = button.getAttribute("data-command");
            const responseOutput = document.getElementById("response-output");

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
    });

    // Handle exit button click
    const exitButton = document.getElementById("exit-button");
    if (exitButton) {
        exitButton.addEventListener("click", () => {
            if (confirm("Are you sure you want to exit?")) {
                window.close(); // Attempt to close the window
            }
        });
    } else {
        console.error('Exit button not found in the DOM.');
    }
});