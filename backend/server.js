const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const { GoogleGenerativeAI } = require("@google/generative-ai");

dotenv.config(); // load .env variables

const app = express();
const port = 5000;

// middleware
app.use(cors());
app.use(express.json());

// initialize Gemini
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// route
app.post("/ask", async (req, res) => {
  try {
    const { question } = req.body;

    if (!question) {
      return res.status(400).json({ error: "Question is required" });
    }

    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(question);

    res.json({ reply: result.response.text() });
  } catch (error) {
    console.error("❌ Error:", error);
    res.status(500).json({ error: "Something went wrong" });
  }
});

// start server
app.listen(port, () => {
  console.log(`✅ Server running on http://localhost:${port}`);
});
