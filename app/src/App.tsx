import React, { useState } from "react";
import type { FormEvent } from "react";
import ReactDOM from "react-dom/client";
import TextBox from "./components/TextBox.tsx"; // Import the TextBox component

const App: React.FC = () => {
  console.log("App.tsx is being rendered!");
  const [question, setQuestion] = useState<string>(""); // State for the question
  const [answer, setAnswer] = useState<string>(""); // State for the answer
  const [error, setError] = useState<string | null>(null); // State for error handling

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent page reload
    console.log("Question submitted:", question);

    if (!question.trim()) {
      setError("Question cannot be empty.");
      setAnswer(""); // Clear the answer if the question is invalid
      return;
    }

    // Here you can add logic to send the question to the backend
    try {
      const response = await fetch("http://localhost:8011/ask", {
        method: "POST",
        // mode: 'no-cors', // Removed to allow proper response handling
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }), // Send the question to the backend
      });

      console.log("Response object:", response);
      
      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer); // Update the answer state with the response
        setError(null); // Clear any previous errors
      } else {
        console.error("Error response:", await response.text()); // Log the error res
        setAnswer("Sorry no answer found"); // Clear the answer if there's an error
      }
    } catch (err) {
      console.error("Error:", err);
      setError("An error occurred. Please check your connection and try again.");
      setAnswer("Sorry we encountered an error"); // Clear the answer if there's an error
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Longevity QA App</h1>
      <p>Type your question below:</p>
      <form onSubmit={handleSubmit}>
        <TextBox
          value={question}
          onChange={(e) => setQuestion(e.target.value)} // Update the question state
          placeholder="Ask a question..."
          label="Your Question:"
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            backgroundColor: "#007BFF",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Submit
        </button>
      </form>
      {answer && (
        <div style={{ marginTop: "20px" }}>
          <h2>Answer:</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default App;


