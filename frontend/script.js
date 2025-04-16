// Ensure DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1; // Track the current page

    const responseOutput = document.getElementById("response-output");
    const logOutput = document.getElementById("log-output");
    const buttonGroup = document.querySelector(".button-group");
    const themeToggle = document.getElementById("theme-toggle");
    const aiToggle = document.getElementById("ai-toggle");
    const aiEngineStatus = document.getElementById("ai-engine-status");
    const progressBar = document.getElementById("loading-progress");
    const progressBarFill = document.getElementById("progress-bar-fill");
    const clearResponseButton = document.getElementById("clear-response");

    // Remove references to the redundant toggle
    const aiEngineToggle = document.getElementById("ai-engine-toggle");

    // Remove any event listeners or logic related to aiEngineToggle
    if (aiEngineToggle) {
        aiEngineToggle.removeEventListener("click", () => {
            // Logic for the redundant toggle (delete this block)
        });
    }

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

    // Function to enable or disable buttons
    function toggleButtons(enable) {
        document.querySelectorAll(".command-button").forEach(button => {
            button.disabled = !enable;
            if (enable) {
                button.classList.remove("disabled");
            } else {
                button.classList.add("disabled");
            }
        });
    }

    // Initially disable buttons
    toggleButtons(false);

    // Handle AI ON/OFF toggle
    aiToggle.addEventListener("click", () => {
        if (aiToggle.classList.contains("status-off")) {
            // Turn ON the AI
            aiToggle.textContent = "Loading...";
            aiToggle.classList.remove("status-off");
            aiToggle.classList.add("status-loading");
            progressBar.classList.remove("hidden");

            // Send request to backend to load AI
            fetch("http://127.0.0.1:5000/ai-engine/on", { method: "POST" })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "loading") {
                        // Simulate progress bar updates
                        let progress = 0;
                        const interval = setInterval(() => {
                            progress += 10;
                            progressBarFill.style.width = `${progress}%`;
                            if (progress >= 100) {
                                clearInterval(interval);
                                aiToggle.textContent = "AI";
                                aiToggle.classList.remove("status-loading");
                                aiToggle.classList.add("status-on");
                                progressBar.classList.add("hidden");

                                // Enable buttons
                                toggleButtons(true);
                            }
                        }, 500);
                    }
                })
                .catch(error => {
                    console.error("Error loading AI:", error);
                    aiToggle.textContent = "AI";
                    aiToggle.classList.remove("status-loading");
                    aiToggle.classList.add("status-off");
                    progressBar.classList.add("hidden");

                    // Ensure buttons remain disabled
                    toggleButtons(false);
                });
        } else {
            // Turn OFF the AI
            aiToggle.textContent = "AI";
            aiToggle.classList.remove("status-on");
            aiToggle.classList.add("status-off");

            // Send request to backend to unload AI
            fetch("http://127.0.0.1:5000/ai-engine/off", { method: "POST" })
                .catch(error => console.error("Error unloading AI:", error));

            // Disable buttons
            toggleButtons(false);
        }
    });

    // Add event listeners for population management
    const initPopulationButton = document.querySelector('[data-command="init population"]');
    const populationModal = document.getElementById("population-modal");
    const deletePopulationButton = document.getElementById("delete-population");
    const growPopulationButton = document.getElementById("grow-population");
    const cancelModalButton = document.getElementById("cancel-modal");

    // Open the modal
    initPopulationButton.addEventListener("click", () => {
        fetch("http://127.0.0.1:5000/check-population", { method: "GET" })
            .then(response => response.json())
            .then(data => {
                if (data.status === "populated") {
                    populationModal.classList.remove("hidden");
                } else {
                    initializePopulation("fresh");
                }
            })
            .catch(error => console.error("Error checking population:", error));
    });

    // Handle user choice
    deletePopulationButton.addEventListener("click", () => {
        initializePopulation("delete");
        populationModal.classList.add("hidden");
    });

    growPopulationButton.addEventListener("click", () => {
        initializePopulation("grow");
        populationModal.classList.add("hidden");
    });

    cancelModalButton.addEventListener("click", () => {
        populationModal.classList.add("hidden");
    });

    // Function to initialize the population
    function initializePopulation(action) {
        const sourceFile = document.getElementById("source-file").value || "codebot_core.py"; // Default to codebot_core.py
        fetch("http://127.0.0.1:5000/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ command: "init population", args: { action, source_file: sourceFile } })
        })
            .then(response => response.json())
            .then(data => alert(data.response))
            .catch(error => console.error("Error initializing population:", error));
    }

    // Function to update the response log
    function updateResponse(message, type = "info") {
        const messageElement = document.createElement("p");
        messageElement.textContent = message;

        // Add a class based on the message type
        if (type === "success") {
            messageElement.classList.add("success");
        } else if (type === "error") {
            messageElement.classList.add("error");
        } else if (type === "warning") {
            messageElement.classList.add("warning");
        }

        responseOutput.appendChild(messageElement);
        responseOutput.scrollTop = responseOutput.scrollHeight; // Auto-scroll to the bottom
    }

    // Clear the response log
    clearResponseButton.addEventListener("click", () => {
        responseOutput.innerHTML = "<p>No response yet.</p>";
    });

    // Example usage
    updateResponse("Population initialized successfully.", "success");
    updateResponse("Error: Source file not found.", "error");
    updateResponse("Warning: Population size is too large.", "warning");

    // Handle "Choose File" button click and form submission
    const chooseFileButton = document.getElementById("choose-file-button");
    const sourceFileInput = document.getElementById("source-file");

    // Handle "Choose File" button click
    chooseFileButton.addEventListener("click", () => {
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = ".py"; // Restrict to Python files
        fileInput.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (file) {
                sourceFileInput.value = file.path; // Display the selected file path
            }
        });
        fileInput.click();
    });

    const initPopulationForm = document.getElementById("init-population-form");

    // Handle form submission
    initPopulationForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(initPopulationForm);
        const params = Object.fromEntries(formData.entries());

        fetch("http://127.0.0.1:5000/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ command: "init population", args: params })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.response);
            })
            .catch(error => console.error("Error initializing population:", error));
    });
});