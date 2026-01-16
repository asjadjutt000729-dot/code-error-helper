// Function to handle the code fixing process using Gemini AI
async function fixCode() {
    // Get the user's input from the textarea
    const codeInput = document.getElementById("codeInput").value;
    
    // Reference UI elements for feedback and results
    const button = document.querySelector("button");
    const resultArea = document.getElementById("resultArea");
    const analysisArea = document.getElementById("analysisArea");
    
    // 1. Validation: Check if the input box is empty
    if (!codeInput.trim()) {
        alert("Please enter some code first!");
        return;
    }

    // 2. UI Feedback: Disable button and show loading status
    button.innerText = "Fixing...";
    button.disabled = true;
    analysisArea.innerText = "Connecting to AI server...";

    try {
        // 3. API Request: Send the code to the FastAPI backend
        // Using a relative path to handle login/static redirection correctly
        const response = await fetch("/fix-code", { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: codeInput })
        });

        // Check if the server responded successfully (Status 200)
        if (!response.ok) throw new Error("Server response was not ok");

        // Parse the JSON data sent back by the backend
        const data = await response.json();
        
        // 4. Update UI: Display the fixed code and success message
        resultArea.innerText = data.fixed_code;
        analysisArea.innerText = "Success: AI has fixed your code!";
        
    } catch (error) {
        // 5. Error Handling: Log errors to console and notify the user
        console.error("Connection Error:", error);
        analysisArea.innerText = "Error: Connection failed. Ensure the FastAPI server is running.";
    } finally {
        // 6. Finalize: Re-enable the button after the process completes
        button.innerText = "Fix My Code";
        button.disabled = false;
    }
}