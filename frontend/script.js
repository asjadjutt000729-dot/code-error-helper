/**
 * Function to handle user login.
 * This is triggered when the Login button is clicked.
 */
async function login() {
    const usernameInput = document.querySelector('input[type="text"]').value;
    const passwordInput = document.querySelector('input[type="password"]').value;
    const errorMessage = document.querySelector('p'); // To show errors on the page

    // Basic validation to ensure fields are not empty
    if (!usernameInput || !passwordInput) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        // Correcting the request path to match the backend
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                username: usernameInput, 
                password: passwordInput 
            })
        });

        if (response.ok) {
            console.log("Login Successful!");
            // Redirect to the dashboard after success
            window.location.href = "/static/index.html";
        } else {
            // Updating the UI to show 'Not Found' or 'Invalid' error
            errorMessage.innerText = "Invalid username or password";
            errorMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Connection error:", error);
        alert("Cannot connect to server. Is the FastAPI server running?");
    }
}

/**
 * Function to send buggy code to Gemini AI for repair.
 */
async function fixCode() {
    const codeInput = document.getElementById("codeInput").value;
    const resultArea = document.getElementById("resultArea");
    const analysisArea = document.getElementById("analysisArea");

    if (!codeInput.trim()) {
        alert("Please enter code first!");
        return;
    }

    try {
        // Using absolute URL to prevent connection issues
        const response = await fetch("http://127.0.0.1:8000/fix-code", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: codeInput })
        });

        const data = await response.json();
        
        if (response.ok) {
            resultArea.innerText = data.fixed_code;
            analysisArea.innerText = "Success: AI has fixed your code!";
        } else {
            analysisArea.innerText = "AI Error: " + data.detail;
        }
    } catch (error) {
        analysisArea.innerText = "Error: Connection failed.";
    }
}