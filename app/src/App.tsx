import React, { useState } from "react";
import type { FormEvent } from "react";
import ReactDOM from "react-dom/client";
import TextBox from "./components/TextBox.tsx"; // Import the TextBox component
import "./styles/App.css"; // Import the CSS file
// import Button from "./components/Button.tsx"; // Import the Button component
import Loader from "./components/Loader.tsx";

/**
 * The main application component for the Longevity Question & Answering App.
 * It allows users to input a question, sends it to the backend for processing,
 * and displays the corresponding answer or error messages.
 */
const LongevityQAApp: React.FC = () => {
  console.log("App.tsx is being rendered!");
  const [question, setQuestion] = useState<string>(""); // State for the question
  const [answer, setAnswer] = useState<string>(""); // State for the answer
  const [error, setError] = useState<string | null>(null); // State for error handling
  const [isLoading, setIsLoading] = useState(false);  //Flag to check if an answer has been received

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent page reload
    console.log("Question submitted:", question);
    setAnswer(`You asked: "${question}"`); // Display the question on the frontend
    setIsLoading(true); // Reset the hasAnswer flag

    if (!question.trim()) {
      setError("Question cannot be empty.");
      setAnswer("No question was provided, please try again!"); // Clear the answer if the question is invalid
      setIsLoading(false); // Reset the hasAnswer flag
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
        setIsLoading(false); // Reset the hasAnswer flag
      } else {
        const errorText = await response.clone().text(); // Clone the response to preserve the body
        console.error("Error response:", errorText); // Log the error response
        setAnswer("Sorry no answer found"); // Clear the answer if there's an error
        setIsLoading(false); // Reset the hasAnswer flag
      }
    } catch (err) {
      console.error("Error:", err);
      setError("An error occurred. Please check your connection and try again.");
      setAnswer("Sorry we encountered an error"); // Clear the answer if there's an error
      setIsLoading(false); // Reset the hasAnswer flag
    }
  };

  return (
    <div className="app-container">
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
      <button 
        type="submit" 
        className="submit-button"
      >
        Submit
      </button>
      </form>
      {answer && (
      <div style={{ marginTop: "20px" }}>
        <h2>Answer:</h2>
        <p>{answer}</p>
        {isLoading && (
            <Loader
              loading={isLoading} // Pass the loading state
              message="Processing your question..." // Custom message
              siz="medium" // Custom size (e.g., "small", "medium", "large")
            />
          )}
      </div>
      )}
    </div>
  );
};

export default LongevityQAApp;


