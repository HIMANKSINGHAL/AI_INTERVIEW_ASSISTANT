# AI Technical Interview Assistant

## Project Structure (single flat folder — no subfolders)

```
build_single_dataset.py         -> run ONCE to generate the dataset
interview_dataset.csv           -> THE single source dataset (raw, with
                                    intentional messiness for cleaning demo)
interview_dataset_clean.csv     -> saved by the notebook after cleaning
                                    (used by app.py to build the question list)
AI_Interview_Assistant.ipynb    -> ALL of: EDA, cleaning, feature engineering,
                                    train/test split, training 6 ML models,
                                    comparison, and saving .pkl artifacts
best_model.pkl                  -> saved by the notebook
label_encoder.pkl               -> saved by the notebook
scaler.pkl                      -> saved by the notebook
tfidf_vectorizer.pkl            -> saved by the notebook
best_model_name.txt             -> saved by the notebook
model_comparison.csv            -> saved by the notebook
app.py                          -> Streamlit UI ONLY. No training logic.
                                    Just loads the .pkl files + cleaned
                                    dataset (all from this same folder)
                                    and renders the interface.
requirements.txt
.gitignore
README.md
```

Every file lives directly in the project's root folder — no `data/` or
`models/` subfolders.

## How to Run

### 1. One-time setup
```bash
pip install -r requirements.txt
```

### 2. (Optional) Regenerate the raw dataset
Only needed if you want to change the questions or regenerate simulated data.
A dataset is already included, so you can skip this.
```bash
python build_single_dataset.py
```

### 3. Run the notebook (does EDA, cleaning, training, saves everything)
Open `AI_Interview_Assistant.ipynb` in VS Code (or Jupyter) and run all cells
top to bottom. This will:
- Load `interview_dataset.csv`
- Show EDA plots (missing values, label distribution, score histogram, etc.)
- Clean the data (drop nulls, dedupe, fix scores, normalize text)
- Engineer 5 ML features
- Train & compare 6 algorithms
- Save the best model + scaler + vectorizer + label encoder into this folder
- Save the cleaned dataset to `interview_dataset_clean.csv`

A version with all cells already executed (with real outputs, plots, and
results) is included, so you don't strictly need to re-run it — but do so
if you change anything.

### 4. Run the app
```bash
streamlit run app.py
```

## Why the app has no training code

`app.py` only calls `pickle.load(...)` on the artifacts the notebook
produced, all sitting in this same folder. If you want to change the model,
features, or dataset, do it in the notebook, re-run it, and restart the app
to pick up the updated `.pkl` files.

## Results (from the included executed notebook run)

| Model | Accuracy |
|---|---|
| SVM | ~80% |
| XGBoost | ~80% |
| KNN | ~79% |
| Random Forest | ~78% |
| Logistic Regression | ~76% |
| Naive Bayes | ~73% |

(Exact numbers vary slightly each time the dataset is regenerated, since
answer simulation involves randomness.)
