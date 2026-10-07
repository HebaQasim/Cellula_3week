GitHub repository: PPV-Prediction-XGBoost
Link: https://github.com/HebaQasim/PPV-Prediction-XGBoost
Description: Predicting PPV values using XGBoost regression model in Python
Main language: Not specified

# PPV Value Prediction using XGBoost

This project applies **Machine Learning (XGBoost)** to predict **PPV (Positive Predictive Value)** from a dataset containing demographic and duration data.  
It was developed as part of the *Artificial Intelligence* course at **Palestine Technical University – Kadoorie**.  

## 📊 Dataset
- **Size:** 5,270 rows × 4 columns  
- **Features:**
  - `Gender` → Categorical (Male/Female)  
  - `Age` → Numerical (int)  
  - `Dur` → Numerical (int, likely duration-related)  
- **Target:**  
  - `PPV` → Continuous numerical variable (float)  



---

## ⚙️ Project Workflow
1. Data loading and exploration (`head()`, `info()`, `describe()`, null checks).  
2. Data cleaning (ensuring valid values for Age and Duration).  
3. One-hot encoding of categorical feature (`Gender`).  
4. Train-test split.  
5. Model training using **XGBRegressor**.  
6. Model evaluation using regression metrics.  
7. Visualization:
   - Scatter plot (predicted vs actual values).  
   - Feature importance analysis.  

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Libraries & Tools:**  
  - `numpy`, `pandas` → data processing  
  - `matplotlib`, `seaborn` → visualization  
  - `scikit-learn` → preprocessing, metrics, train-test split  
  - `xgboost` → model training  

