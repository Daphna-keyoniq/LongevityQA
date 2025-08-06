import React, { useState, useCallback } from "react";
import "./../styles/PredefinedQA.css"; // Import styles for the component
import { HiOutlineChevronDoubleDown, HiOutlineChevronDoubleRight } from "react-icons/hi";
import { AiOutlineDown, AiOutlineRight } from "react-icons/ai";

// Define the predefined questions and answers directly in the file
const predefinedQAData = [
  {
    category: "General Information",
    question: "Longevity",
    answer: "Longevity medicine is a field of medicine that focuses on extending the healthy lifespan of individuals, with a proactive approach to healthcare. The focus being on preventing diseases, delaying the process of aging, and promoting overall well-being, rather than treating diseases after they occur."
  },
  {
    category: "General Information",
    question: "Healthspan?",
    answer: "Healthspan is the number of years in which one lives in good health and has a high quality of life, free from chronic diseases and disabilities. It emphasizes living better and healthier for longer."
  },
  {
    category: "General Information",
    question: "Preventative and Proactive Healthcare",
    answer: "Preventative care focuses on early detection and prevention of health risks before they develop into disorders, through early screening, testing, and lifestyle modifications. Proactive healthcare goes a step further by actively managing health through personalised lifestyle adjustments and advanced medical therapies, to not only prevent diseases not only before the occur, but before there is a disease risk. Preventative care would for example be putting someone who is obese and pre-diabetic on a weight loss program, while proactive healthcare would be incorporating and exercise regime and healthy diet even before signs of metabolic issues arise."
  },
  {
    category: "General Information",
    question: "Blue Zones",
    answer: "Blue Zones are regions where residents have a high life expectancy and low rate of chronic disease. These areas are studied for their lifestyle, diet, and social habits that contribute to longevity. In his book, The Blue Zones, Buettner describes five known Blue Zones: 1) Icaria (Greece): Resdinets of this greek island eat a Mediterranean diet. 2) Ogliastra, Sardinia (Italy): The long-living residents of this region typically work on farms and drink lots of red wine. 3) Okinawa (Japan): where residents eat a lot of soy-based foods and practice tai chi. 4) Nicoya Peninsula (Costa Rica): the Nicoyans eat a lot of beans and corn tortillas, perform physical jobs into old age and have a strong sense of life purpose. 5) The Seventh-day Adventists in Loma Linda, California (USA): Residents are very religious, strict vegetarians and live in tight-knit communities."
  },
  {
    category: "General Information",
    question: "Which longevity treatments do you offer?",
    answer: "Longevity treatments include lifestyle modifications, nutritional interventions, exercise programs, supplements, and advanced medical therapies. Some longevity medications exist, often in the form of repurposed drugs, with new evidence coming out that these medications also have a positive effect of slowing down aging."
  },
  {
    category: "General Information",
    question: "The 6 pillars of longevity",
    answer: "The 6 pillars of longevity are: 1) Nutrition: A balanced diet rich in whole foods, fruits, vegetables, and healthy fats. 2) Exercise & physical activity, including both aerobic and resistance training. 3) Quality Sleep. 4) Mental & Emotional Health, with a focus on happinnes and emotional wellbeing, through stress reduction methods, mindfulness, meditation, and relaxation to reduce stress. 5) Social Connections: Maintaining strong relationships and positive social interactions. 6) Supplements & Medications, and avoidance of harmful substances."
  },
  {
    category: "Longevity Medications",
    question: "What are repurposed longevity drugs?",
    answer: "Repurposed longevity drugs, such as metformin and rapamycin, refer to medications that were developed and approved for one disease, and later found to also be useful as longevity medications. Resaerch on these drugs as longevity treatments is larger new, and often still ongoing, but they have shown promise in extending lifespan and healthspan in various studies."
  }, 
  {
    category: "Longevity Medications",
    question: "Tell me about Metformin",
    answer: "Metformin is a medication primarily used to treat type 2 diabetes, that has recently also gained interest as a longevity medicine due to its potential effects on aging and healthspan extension. Research suggests that metformin may improve metabolic health, reduce inflammation, and mimic some effects of caloric restriction, which are beneficial for longevity. It is being studied for its potential to delay age-related diseases in humans."
  }, 
  {
    category: "Longevity Medications",
    question: "Tell me about Rapamycin",
    answer: "Rapamycin, also known as Sirolimus, is an mTOR inhibitor increasingly being considered as a universal longevity drug. It was originally developed as an antifungal drug, and later also as an immunosuppressant. It is known to inhibit the mTOR pathway, which is involved in cell growth and aging processes. In longevity medicine, Rapamycin is explored for its potential to delay aging and age-related diseases."
  }, 
  {
    category: "Supplements",
    question: "Which supplements should I take?",
    answer: "Supplement recommendations are highly individual and may depend on your personal health status, health needs, and demographic factors. We therefore recommend building a persoanlised longevity plan that can target your individual concerns and goals. Supplements that are commonly used in longevity practice are Omega-3, CoQ10, Nicotinamide, Vitamin D, Creatine, Berberine, Magnesium and more."
  },
  {
    category: "Supplements",
    question: "Which supplements are beneficial for metabolic health?",
    answer: "Omega-3 fatty acids, Berberine, Chromium, Alpha-Lipoic Acid, and Magnesium. These supplements can help improve insulin sensitivity, reduce inflammation, and support overall metabolic function."
  },  
  {
    category: "Supplements",
    question: "Which supplements can help maintain long-term bone density?",
    answer: "Supplements that can help maintain long-term bone density include Vitamin D, Calcium, Magnesium, Vitamin K2, and Boron. These nutrients play crucial roles in bone health by supporting calcium absorption, bone mineralization, and overall skeletal strength."
  },  
  {
    category: "Supplements",
    question: "What is Berberine good for?",
    answer: "Berberine is anti-inflammatory and has potential benefits for metabolic health, including blood sugar regulation, cholesterol levels, and weight management. It may also help improve cardiovascular health and gut microbiome balance."
  }, 
  {
    category: "Exercise",
    question: "Aerobic vs. Resistance Training",
    answer: "The two main types of exercise are aerobic (cardiovascular) and anaerobic strength training, also called resistance training. Aerobic exercise includes activities like running, swimming, and cycling, which improve cardiovascular health and endurance. Anaerobic exercise includes weightlifting and resistance training, which build muscle strength and mass."
  },
  {
    category: "Nutrition",
    question: "Sugar",
    answer: "Sugar, particularly added sugars, can have negative effects on health, including increased risk of obesity, type 2 diabetes, and heart disease. It is recommended to limit added sugars in the diet and focus on whole foods with natural sugars, such as fruits."
  }, 
  {
    category: "Nutrition",
    question: "Leafy Greens",
    answer: "Leafy greens, such as spinach, kale, and Swiss chard, are rich in vitamins, minerals, and antioxidants. They are low in calories and high in fiber, making them beneficial for weight management and overall health. Regular consumption of leafy greens is associated with reduced risk of chronic diseases."
  }, 
  {
    category: "Nutrition",
    question: "Olive Oil",
    answer: "Olive oil is a staple of the Mediterranean diet and is known for its health benefits, including anti-inflammatory properties, heart health support, and potential longevity benefits. It is rich in monounsaturated fats and antioxidants, making it a healthy choice for cooking and salad dressings."
  }, 
  {
    category: "Nutrition",
    question: "Protein",
    answer: "Protein is also important for longevity and maintaining strength as you age. When you eat protein from food, it’s broken down into individual amino acids, and these amino acids are used to form the structural elements of your body such as muscles, tendons, ligaments, and collagen.  Without adequate protein, you may be at increased risk for sarcopenia, i.e. age-related muscle loss, which, in turn, may impair physical activity and increase risk of falls and death. Consuming adequate protein also helps prevent dangerous spikes in blood sugar."
  }, 
  {
    category: "Age-Related Diseases",
    question: "What are the most common age-related diseases?",
    answer: "The most common age-related diseases include cardiovascular diseases, diabetes, Alzheimer's disease and other dementias, osteoporosis, arthritis, and certain cancers. These conditions are often associated with aging and can significantly impact quality of life."
  }, 
  {
    category: "Age-Related Diseases",
    question: "Type 2 Diabetes",
    answer: "Type 2 diabetes is a chronic condition that affects the way the body processes blood sugar (glucose). It is characterized by insulin resistance, where the body's cells do not respond effectively to insulin, leading to elevated blood sugar levels. Lifestyle changes, such as diet and exercise, along with medications, can help manage the condition."
  }, 
  {
    category: "Age-Related Diseases",
    question: "Cardiovascular Diseases",
    answer: "Cardiovascular diseases (CVD) are a group of disorders affecting the heart and blood vessels, including coronary artery disease, heart failure, and stroke. They are often caused by a combination of genetic factors, lifestyle choices, and other health conditions. Prevention and management include lifestyle changes, medications, and sometimes surgical interventions."
  }, 
  {
    category: "Age-Related Diseases",
    question: "Sarcoopenia",
    answer: "Sarcopenia is the age-related loss of muscle mass and strength, which can lead to frailty, falls, and decreased mobility. It is a significant health concern in older adults and can be mitigated through resistance training, adequate protein intake, and overall physical activity."
  }, 
  {
    category: "Age-Related Diseases",
    question: "Osteoporosis",
    answer: "Osteoporosis causes bones to become weak and brittle — so brittle that a fall or even mild stresses such as bending over or coughing can cause a break. Osteoporosis-related breaks most commonly occur in the hip, wrist or spine. At higher risk for Osteoporosis are post-menopausal women."
  }, 
  {
    category: "Age-Related Diseases",
    question: "Alzeheimer's Disease and Dementia",
    answer: "Alzheimer's disease is a progressive neurological disorder that causes brain cells to degenerate and die, leading to memory loss, cognitive decline, and changes in behavior. Dementia is a broader term that encompasses various conditions, including Alzheimer's, characterized by a decline in cognitive function severe enough to interfere with daily life."
  }, 
  {
    category: "Age-Related Diseases",
    question: "Parkinson's Disease",
    answer: "Parkinson's disease is a progressive neurological disorder that affects movement. It occurs when nerve cells in the brain that produce dopamine, a neurotransmitter that helps control movement, become impaired or die. Symptoms include tremors, stiffness, and difficulty with balance and coordination."
  }, 
];

const PredefinedQA: React.FC = () => {
  const [openCategory, setOpenCategory] = useState<string | null>("General Information"); // Default open category
  const [openQuestionIndex, setOpenQuestionIndex] = useState<number | null>(null);

  // Group questions by category dynamically
  const groupedQuestions = predefinedQAData.reduce((acc, qa) => {
    if (!acc[qa.category]) {
      acc[qa.category] = [];
    }
    acc[qa.category].push(qa);
    return acc;
  }, {} as { [key: string]: typeof predefinedQAData });

  // Toggle visibility of a category
  const toggleCategory = useCallback(
    (category: string) => {
      setOpenCategory((prevCategory) => (prevCategory === category ? null : category));
    },
    []
  );

  // Toggle visibility of an individual question
  const toggleAnswer = useCallback(
    (index: number) => {
      setOpenQuestionIndex((prevIndex) => (prevIndex === index ? null : index));
    },
    []
  );

  return (
    <div className="predefined-qa-container">
      <h1>About Longevity</h1>
      {Object.keys(groupedQuestions).map((category) => (
        <div key={category} className="qa-category">
          {/* Category title with toggle arrow */}
        <h2
          className={`category-title ${openCategory === category ? "active" : ""}`}
          onClick={() => toggleCategory(category)}
          style={{ cursor: "pointer", display: "flex", alignItems: "center" }}
        >
          <span style={{ marginRight: "8px" }}>
            {openCategory === category ? <AiOutlineDown /> : <AiOutlineRight />
            }
          </span>
          <span>{category}</span>
        </h2>
          {/* Questions under the category */}
          {openCategory === category && (
            <div className="qa-list">
              {groupedQuestions[category].map((qa, index) => (
                <div key={index} className="qa-item">
                  <div
                              className={`question ${openQuestionIndex === index ? "active" : ""}`}

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
          )}
        </div>
      ))}
    </div>
  );
};

export default PredefinedQA;