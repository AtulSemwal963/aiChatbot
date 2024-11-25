const express = require("express");
const axios = require("axios");
const cors = require("cors");
const app = express();


app.use(express.json()); // For parsing JSON request bodies
app.use(cors());  // Enable CORS for all routes

// Define the route for chatbot communication
app.post("/chat", async (req, res) => {
    const userInput = req.body.userInput;

    try {
        // Send the user input to the Python chatbot API
        const response = await axios.post("http://127.0.0.1:8000/chat", {
            user_input: userInput
        });

        // Return the chatbot response to the client
        res.json({ botResponse: response.data.bot_response });
    } catch (error) {
        console.error("Error communicating with Python API:", error.message);
        res.status(500).send("Error communicating with the chatbot.");
    }
});

// Start the Node.js server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Node.js server is running on http://127.0.0.1:${PORT}`);
});
