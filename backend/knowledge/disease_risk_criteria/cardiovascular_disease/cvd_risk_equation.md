# CVD Risk Calculator Equation

## Equation
Below is the math that this calculator uses to get CVD risk scores:

Terms = (C_Age * ln(Age)) + (C_Sq_Age * sq(ln(Age))) + (C_Total_Chol * ln(Total_cholesterol)) + (C_Age_Total_Chol * ln(Age) * ln(Total_cholesterol)) + (C_HDL_Chol * ln(HDL_cholesterol)) + (C_Age_HDL_Chol * ln(Age) * ln(HDL_cholesterol)) + (Do you take blood pressure medication? * C_Do you take blood pressure medication?s * ln(Systolic blood pressure)) + (Do you take blood pressure medication? * C_Age_Do you take blood pressure medication?s * ln(Age) * ln(Systolic blood pressure)) + (not Do you take blood pressure medication? * C_Off_Hypertension_Meds * ln(Systolic blood pressure)) + (not Do you take blood pressure medication? * C_Age_Off_Hypertension_Meds * ln(Age) * ln(Systolic blood pressure)) + (C_Do you smoke cigarettes? * Do you smoke cigarettes?) + (C_Age_Do you smoke cigarettes? * ln(Age) * Do you smoke cigarettes?) + (C_Do you have diabetes? * Do you have diabetes?) Risk = 100 * (1 - S10e(Terms-Mean_Terms))


## Calculation Details and Variables

For **Black or African American female patients**:
- `CAge = 17.114`
- `CSqAge = 0`
- `CTotalChol = 0.94`
- `CAgeTotalChol = 0`
- `CHDLChol = -18.92`
- `CAgeHDLChol = 4.475`
- `COnHypertensionMeds = 29.291`
- `CAgeOnHypertensionMeds = -6.432`
- `COffHypertensionMeds = 27.82`
- `CAgeOffHypertensionMeds = -6.087`
- `CSmoker = 0.691`
- `CAgeSmoker = 0`
- `CDiabetes = 0.874`
- `S10 = 0.9533`
- `MeanTerms = 86.61`

For **White or other race female patients**:
- `CAge = -29.799`
- `CSqAge = 4.884`
- `CTotalChol = 13.54`
- `CAgeTotalChol = -3.114`
- `CHDLChol = -13.578`
- `CAgeHDLChol = 3.149`
- `COnHypertensionMeds = 2.019`
- `CAgeOnHypertensionMeds = 0`
- `COffHypertensionMeds = 1.957`
- `CAgeOffHypertensionMeds = 0`
- `CSmoker = 7.574`
- `CAgeSmoker = -1.665`
- `CDiabetes = 0.661`
- `S10 = 0.9665`
- `MeanTerms = -29.18`

For **Black or African American male patients**:
- `CAge = 2.469`
- `CSqAge = 0`
- `CTotalChol = 0.302`
- `CAgeTotalChol = 0`
- `CHDLChol = -0.307`
- `CAgeHDLChol = 0`
- `COnHypertensionMeds = 1.916`
- `CAgeOnHypertensionMeds = 0`
- `COffHypertensionMeds = 1.809`
- `CAgeOffHypertensionMeds = 0`
- `CSmoker = 0.549`
- `CAgeSmoker = 0`
- `CDiabetes = 0.645`
- `S10 = 0.8954`
- `MeanTerms = 19.54`

For **White or other race male patients**:
- `CAge = 12.344`
- `CSqAge = 0`
- `CTotalChol = 11.853`
- `CAgeTotalChol = -2.664`
- `CHDLChol = -7.99`
- `CAgeHDLChol = 1.769`
- `COnHypertensionMeds = 1.797`
- `CAgeOnHypertensionMeds = 0`
- `COffHypertensionMeds = 1.764`
- `CAgeOffHypertensionMeds = 0`
- `CSmoker = 7.837`
- `CAgeSmoker = -1.795`
- `CDiabetes = 0.658`
- `S10 = 0.9144`
- `MeanTerms = 61.18`

## Notes

- This calculator is intended for people between the ages of 40 and 79. It helps predict your risk over 10 years of heart attack, stroke, or death from cardiovascular disease.
- Your doctor can help you understand your personal risk and how to interpret your results. The calculator cannot tell for sure whether you will have a cardiovascular event.
- This calculator was developed based on data from primarily white and African American people. If you are of a different background, the calculator may underestimate or overestimate your risk.
- Systolic blood pressure is the top number (e.g., 120 if blood pressure is 120/80).
- **ACC**: American College of Cardiology; **AHA**: American Heart Association; **HDL**: high-density lipoprotein.
- Only digits 0 to 9 and a single decimal point (".") are acceptable as numeric inputs. Attempted input of other characters into a numeric field may lead to an incorrect result.
- Information on this page may not appear correctly if printed.

## References

Goff DC Jr, Lloyd-Jones DM, Bennett G, et al. 2013 ACC/AHA Guideline on the Assessment of Cardiovascular Risk: A Report of the American College of Cardiology/American Heart Association Task Force on Practice Guidelines. Circulation 2014; 129:S49.

## Source
source type: website
source link: uptodate.com/contents/calculator-cardiovascular-risk-assessment-in-adults-10-year-acc-aha-2013-patient-education