import React, { useState, useCallback } from "react";
import "./../styles/PredefinedQA.css"; // Import styles for the component

// Define the predefined questions and answers directly in the file
const predefinedQAData = [
  {
    question: "What is longevity?",
    answer: "Longevity care is a field of medicine that focuses on extending the healthy lifespan of individuals, with a proactive approach to healthcare. The focus being on preventing diseases, delaying the process of aging, and promoting overall well-being, rather than treating diseases after they occur."
  },
  {
    question: "How is healthspan?",
    answer: "Healthspan is the number of years in which one lives in good health and has a high quality of life, free from chronic diseases and disabilities. It emphasizes living better and healthier for longer."
  },
  {
    question: "What main longevity treatments are offered?",
    answer: "Longevity treatments include lifestyle modifications, nutritional interventions, exercise programs, supplements, and advanced medical therapies. Some longevity medications exist, often in the form of repurposed drugs, with new evidence coming out that these medications also have a positive effect of slowing down aging."
  },
  {
    question: "What are repurposed longevity drugs?",
    answer: "Repurposed longevity drugs, such as metformin and rapamycin, refer to medications that were developed and approved for one disease, and later found to also be useful as longevity medications. Resaerch on these drugs as longevity treatments is larger new, and often still ongoing, but they have shown promise in extending lifespan and healthspan in various studies."
  }, 
  {
    question: "What is Metformin?",
    answer: "Repurposed longevity drugs, such as metformin and rapamycin, refer to medications that were developed and approved for one disease, and later found to also be useful as longevity medications. Resaerch on these drugs as longevity treatments is larger new, and often still ongoing, but they have shown promise in extending lifespan and healthspan in various studies."
  }, 
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