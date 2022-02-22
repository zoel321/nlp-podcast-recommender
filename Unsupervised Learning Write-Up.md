##  Classification Project Write-Up

**Abstract**

The goal of this project was to use classification to predict rehospitalization (either <30 days or >30 days, vs. no rehospitalization) using the US Hospitals 1999-2008 Diabetes dataset, which consists of de-identified healthcare data for inpatient visits. Random forest, logistic regression, and XGBoost models were tried. After using the final logistic regression model to predict rehospitalization on the test data, the F1 score was 0.529 while the accuracy was 60.57%.

**Design**

This project’s data came from the Center for Clinical and Translational Research at Virginia University. Although the data contains older information, it may provide some insights as to which factors (patient or hospital encounter-related) during an inpatient visit can contribute to predicting readmission. Preventing readmissions is not only beneficial for patients and their providers, who can dedicate their efforts to new admissions, but also for managed care organizations who want to avoid unnecessary healthcare expenditures. 

The F1 metric was prioritized for model comparison, as minimizing false negatives (for the purpose of targeting suitable interventions) and false positives (for cost) were important for the goal. The target class distribution was also imbalanced after data cleaning, which would likely be the case in other comparable datasets. 

**Data**

The initial dataset contained over 100,000 rows/encounters with over 50 features. These included: race, gender, age, admission type, time in hospital, medical specialty of admitting physician, number of lab test performed, HbA1c test result, diagnosis, number of medications, diabetes medications, number of outpatient, inpatient, and emergency visits in the year before the hospitalization, etc. To reduce confounding, only one encounter (the first encounter) was included for each unique patient. Patients who had a discharge status labeled as hospice, expired, or missing were also removed.

**Algorithms**

Feature Engineering:

\-    Grouping medication classes then binarizing (same dose/not on med = 0, increase/decrease dose = 1)

\-    Turning categorical variables into dummy variables: Admission Type, A1C, Max Glucose, Diagnoses 1/2/3, Age Group

\-    Interaction: Diagnosis of heart failure and on TZD-class medication for diabetes 

Models:

Logistic regression, random forest, and XGBoost classifiers were tuned and cross-validated (80/20 train vs. holdout). A logistic regression model was selected for the final test evaluation, due to its highest F1 score (0.5218) and comparable accuracy (59.78%)  and ROC AUC values (0.628), along with its interpretability. On the holdout set, the F1 score was 0.5294 and the accuracy score was 60.57%. The top five features (largest coefficients) in the final model were: Age 70-80, 60-80, number of inpatient visits in preceding year, Age 80-90, followed by Age 50-60. This was similar in terms of features with the largest SHAP values, except “Emergency Department admission type” is included as a top feature. 

**Tools**

- Pandas for data analysis/cleaning
- Scikit-learn for modeling steps
- Matplotlib, Seaborn and SHAP for plotting/visualizations

**Communication**

The results and code are in this repo, along with the final slides. A Tableau Public dashboard may be embedded in a future blog post.





