// Ensure DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1; // Track the current page

    const responseOutput = document.getElementById("response-output");
    const logOutput = document.getElementById("log-output");
    const buttonGroup = document.querySelector(".button-group");
    const themeToggle = document.getElementById("theme-toggle");

    // Initialize theme based on local storage
    const isDarkTheme = localStorage.getItem("dark-theme") === "true";
    document.body.classList.toggle("dark-theme", isDarkTheme);
    themeToggle.textContent = isDarkTheme ? "🌙" : "☀";

    // Function to send commands to the backend
    function sendCommand(command, args = {}) {
        fetch("http://127.0.0.1:5000/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ command, args })
        })
            .then(response => response.json())
            .then(data => {
                responseOutput.textContent = data.response;
                if (data.data) {
                    logOutput.innerHTML += `<pre>${JSON.stringify(data.data, null, 2)}</pre>`;
                }
            })
            .catch(error => {
                responseOutput.textContent = `Error: ${error.message}`;
            });
    }

    // Function to fetch and display individuals
    function fetchIndividuals(page = 1) {
        sendCommand("evaluate population", { page });
    }

    // Add event listener for the "Evaluate Population" button
    buttonGroup.querySelector('[data-command="evaluate population"]').addEventListener("click", () => {
        currentPage = 1; // Reset to the first page
        fetchIndividuals(currentPage);
    });

    // Handle "Send" button click
    const sendCommandButton = document.getElementById("send-command");
    if (sendCommandButton) {
        sendCommandButton.addEventListener("click", () => {
            const commandInput = document.getElementById("command-input");
            const command = commandInput ? commandInput.value.trim().toLowerCase() : "";

            if (!command) {
                responseOutput.textContent = "Please enter a command.";
                return;
            }

            sendCommand(command);
        });
    } else {
        console.error('Send command button not found in the DOM.');
    }

    // Add event listeners for command buttons
    document.querySelectorAll(".command-button").forEach(button => {
        button.addEventListener("click", () => {
            const command = button.getAttribute("data-command");
            sendCommand(command);
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

    // Add event listener for theme toggle
    themeToggle.addEventListener("click", () => {
        const isDark = document.body.classList.toggle("dark-theme");
        localStorage.setItem("dark-theme", isDark);
        themeToggle.textContent = isDark ? "🌙" : "☀";
    });
});