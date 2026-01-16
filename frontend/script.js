/**
 * Function to handle the code fixing process using Gemini AI.
 * It connects the frontend UI with the FastAPI backend.
 */
async function fixCode() {
    // 1. INPUT RETRIEVAL: Get the user's code from the textarea
    const codeInput = document.getElementById("codeInput").value;
    
    // UI element references for feedback and results
    const button = document.querySelector("button");
    const resultArea = document.getElementById("resultArea");
    const analysisArea = document.getElementById("analysisArea");
    
    // 2. VALIDATION: Ensure the input is not empty before sending
    if (!codeInput.trim()) {
        alert("Please enter some code first!");
        return;
    }

    // 3. UI FEEDBACK: Disable the button and show loading status to the user
    button.innerText = "Fixing...";
    button.disabled = true;
    analysisArea.innerText = "Connecting to AI server...";

    try {
       // Send the code to the FastAPI backend using the absolute local server URL
// Using 'http://127.0.0.1:8000' ensures the browser knows exactly where the API is running
const response = await fetch("http://127.0.0.1:8000/fix-code", { 
    // Set the request method to POST as required by the backend endpoint
    method: "POST",
    
    // Define the headers to tell the server we are sending JSON data
    headers: { "Content-Type": "application/json" },
    
    // Convert the Python code from the input box into a JSON string for transmission
    body: JSON.stringify({ code: codeInput })
});

        // Check if the server responded successfully (HTTP Status 200)
        if (!response.ok) {
            throw new Error("Server response was not ok. Status: " + response.status);
        }

        // Parse the JSON response sent back by the backend
        const data = await response.json();
        
        // 5. UPDATE UI: Display the fixed code and success message
        resultArea.innerText = data.fixed_code;
        analysisArea.innerText = "Success: AI has fixed your code!";
        
    } catch (error) {
        // 6. ERROR HANDLING: Log connection issues and notify the user
        console.error("Connection Error:", error);
        analysisArea.innerText = "Error: Connection failed. Ensure the FastAPI server is running.";
    } finally {
        // 7. FINALIZE: Re-enable the button once the process is complete
        button.innerText = "Fix My Code";
        button.disabled = false;
    }
}