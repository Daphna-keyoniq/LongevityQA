import React, { useState } from "react";
import type { FormEvent } from "react";
import ReactDOM from "react-dom/client";
import TextBox from "./components/TextBox.tsx"; // Import the TextBox component
import Button from "./components/Button.tsx"; // Import the Button component

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

    try {
      const response = await fetch("http://172.161.85.236:8011/ask", {
        method: "POST",
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
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", color:"#54769D"}}>
      <h1>Longevity QA</h1>
      <p>Welcome to the Longevity Question & Answering App! 
      <br />
        Please type your question below:</p>
      <form onSubmit={handleSubmit}>
        <TextBox
          value={question}
          onChange={(e) => setQuestion(e.target.value)} // Update the question state
          placeholder="Ask a question..."
          label="Your Question:"
        />
        <Button> Submit</Button>
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


