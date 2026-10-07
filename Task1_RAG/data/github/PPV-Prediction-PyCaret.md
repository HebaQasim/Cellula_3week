GitHub repository: PPV-Prediction-PyCaret
Link: https://github.com/HebaQasim/PPV-Prediction-PyCaret
Description: No description
Main language: Not specified

# PPV Value Prediction using PyCaret

This project applies **PyCaret (an open-source low-code ML library in Python)** to predict **PPV (Positive Predictive Value)** from a dataset containing demographic and duration data.  
It was developed as part of the *Machine Learning* course at **Palestine Technical University – Kadoorie**.  

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
4. **PyCaret Setup:** initialized regression environment with PPV as target.  
5. **Model Comparison:** `compare_models()` → selected **Random Forest Regressor** as best.  
6. Model evaluation with PyCaret’s interactive `evaluate_model()`.  
7. Predictions on new/unseen data.  
8. Final trained model saved for reuse.  

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Libraries & Tools:**  
  - `numpy`, `pandas` → data processing  
  - `matplotlib`, `seaborn` → visualization  
  - `pycaret` → model comparison, training, evaluation  
  - `scikit-learn` → backend ML utilities  
