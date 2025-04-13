// Ensure DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1; // Track the current page

    const responseOutput = document.getElementById("response-output");
    const buttonGroup = document.querySelector(".button-group");

    // Function to fetch and display individuals
    function fetchIndividuals(page = 1) {
        fetch("http://127.0.0.1:5000/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ command: "evaluate population", page })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Display the list of genetic individuals
                const individuals = data.data;
                let listHtml = `<h3>${data.response}</h3><ul>`;
                individuals.forEach(individual => {
                    listHtml += `<li>${individual.name}</li>`;
                });
                listHtml += "</ul>";

                // Add pagination buttons
                listHtml += `
                    <div class="pagination-buttons">
                        <button id="home-button" ${currentPage === 1 ? "disabled" : ""}>Home</button>
                        <button id="prev-button" ${currentPage === 1 ? "disabled" : ""}>Previous</button>
                        <button id="next-button" ${currentPage === data.total_pages ? "disabled" : ""}>Next</button>
                    </div>
                `;

                responseOutput.innerHTML = listHtml;

                // Add event listeners for pagination buttons
                document.getElementById("home-button").addEventListener("click", () => {
                    currentPage = 1;
                    fetchIndividuals(currentPage);
                });
                document.getElementById("prev-button").addEventListener("click", () => {
                    if (currentPage > 1) {
                        currentPage--;
                        fetchIndividuals(currentPage);
                    }
                });
                document.getElementById("next-button").addEventListener("click", () => {
                    if (currentPage < data.total_pages) {
                        currentPage++;
                        fetchIndividuals(currentPage);
                    }
                });
            })
            .catch(error => {
                responseOutput.textContent = `Error: ${error.message}`;
            });
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