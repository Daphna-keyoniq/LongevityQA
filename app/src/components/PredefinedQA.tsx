import React, { useState, useCallback } from "react";
import "./../styles/PredefinedQA.css"; // Import styles for the component

// Define the predefined questions and answers directly in the file
const predefinedQAData = [
  {
    question: "What is longevity?",
    answer: "Longevity refers to the length of time that an individual lives."
  },
  {
    question: "How can I improve my longevity?",
    answer: "You can improve your longevity by maintaining a healthy lifestyle, exercising, and eating a balanced diet."
  },
  {
    question: "What are the key factors affecting longevity?",
    answer: "Key factors include genetics, lifestyle, environment, and access to healthcare."
  }
];

const PredefinedQA: React.FC = () => {
  const [openQuestionIndex, setOpenQuestionIndex] = useState<number | null>(null);

  // Use useCallback to memoize the toggle function and prevent unnecessary re-renders
  const toggleAnswer = useCallback(
    (index: number) => {
      setOpenQuestionIndex((prevIndex) => (prevIndex === index ? null : index));
    },
    []
  );

  return (
    <div className="predefined-qa-container">
      <h1>About Longevity</h1>
      {predefinedQAData.map((qa, index) => (
        <div key={index} className="qa-item">
          <div
            className="question"
            onClick={() => toggleAnswer(index)}
          >
            {qa.question}
          </div>
          {openQuestionIndex === index && (
            <div className="answer">{qa.answer}</div>
          )}
        </div>
      ))}
    </div>
  );
};

export default PredefinedQA;