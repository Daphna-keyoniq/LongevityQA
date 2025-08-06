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
    question: "What are the Blue Zones?",
    answer: "Blue Zones are regions of the world where people are reported to live much longer than average. These areas are studied for their lifestyle, diet, and social habits that contribute to longevity."
  }
  {
    question: "What main longevity treatments are offered?",
    answer: "Longevity treatments include lifestyle modifications, nutritional interventions, exercise programs, supplements, and advanced medical therapies. Some longevity medications exist, often in the form of repurposed drugs, with new evidence coming out that these medications also have a positive effect of slowing down aging."
  },
  {
    question: "What are repurposed longevity drugs?",
    answer: "Repurposed longevity drugs, such as metformin and rapamycin, refer to medications that were developed and approved for one disease, and later found to also be useful as longevity medications. Resaerch on these drugs as longevity treatments is larger new, and often still ongoing, but they have shown promise in extending lifespan and healthspan in various studies."
  }, 
  {
    question: "Tell me about Metformin",
    answer: "Metformin is a medication primarily used to treat type 2 diabetes, that has recently also gained interest as a longevity medicine due to its potential effects on aging and healthspan extension. Research suggests that metformin may improve metabolic health, reduce inflammation, and mimic some effects of caloric restriction, which are beneficial for longevity. It is being studied for its potential to delay age-related diseases in humans."
  }, 
  {
    question: "Tell me about Rapamycin",
    answer: "Rapamycin, also known as Sirolimus, is an mTOR inhibitor increasingly being considered as a universal longevity drug. It was originally developed as an antifungal drug, and later also as an immunosuppressant. It is known to inhibit the mTOR pathway, which is involved in cell growth and aging processes. In longevity medicine, Rapamycin is explored for its potential to delay aging and age-related diseases."
  }, 
  {
    question: "Which supplements should I take?",
    answer: "Supplementat recommendations are highly individual and may depend on your personal health status, health needs, and demographic factors. We therefore recommend building a persoanlised longevity plan that can target your individual concerns and goals. Supplements that are commonly used in longevity practice are Omega-3, CoQ10, Nicotinamide, Vitamin D, Creatine, Berberine, Magnesium and more."
  }, 
  {
    question: "Which supplements should I take?",
    answer: "Supplementat recommendations are highly individual and may depend on your personal health status, health needs, and demographic factors. We therefore recommend building a persoanlised longevity plan that can target your individual concerns and goals. Supplements that are commonly used in longevity practice are Omega-3, CoQ10, Nicotinamide, Vitamin D, Creatine, Berberine, Magnesium and more."
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