// Ensure DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Handle "Send" button click
    const sendCommandButton = document.getElementById("send-command");
    if (sendCommandButton) {
        sendCommandButton.addEventListener("click", () => {
            const commandInput = document.getElementById("command-input");
            const command = commandInput ? commandInput.value.trim().toLowerCase() : "";
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
    } else {
        console.error('Send command button not found in the DOM.');
    }

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
                    if (command === "evaluate population" && data.data) {
                        // Display the list of genetic individuals
                        const individuals = data.data;
                        let listHtml = "<ul>";
                        individuals.forEach(individual => {
                            listHtml += `<li>${individual.name} (Fitness: ${individual.fitness})</li>`;
                        });
                        listHtml += "</ul>";
                        responseOutput.innerHTML = listHtml;
                    } else {
                        // Display the response for other commands
                        responseOutput.textContent = data.response;
                    }
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
                // Redirect to a goodbye page or display a message
                document.body.innerHTML = `
                    <div style="text-align: center; margin-top: 50px;">
                        <h1>Goodbye!</h1>
                        <p>Thank you for using CodeBot. You can close this tab now.</p>
                    </div>
                `;
            }
        });
    } else {
        console.error('Exit button not found in the DOM.');
    }
});