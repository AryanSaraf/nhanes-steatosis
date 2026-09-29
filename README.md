# NHANES Hepatic Steatosis Screening

This project uses NHANES data to investigate whether routinely available demographic and metabolic variables can identify adults with hepatic steatosis.

The initial analysis uses the **NHANES 2017–March 2020 pre-pandemic dataset**. The **2021–2023 NHANES cycle** is reserved for later validation.

## Project Structure

```text
nhanes-steatosis/
├── data/
│   ├── raw/
│   │   ├── 2017-2020/       # Original NHANES XPT files
│   │   └── 2021-2023/       # Future validation data
│   └── processed/            # Cleaned and merged datasets
├── notebooks/                # Analysis notebooks
├── src/                      # Downloading and processing scripts
├── results/                  # Model results, tables, and figures
└── README.md
```
## Datasets

We use the **NHANES 2017–March 2020 pre-pandemic** datasets for the main analysis.

NHANES stores different types of information in separate XPT files. We selected the following datasets because together they contain the outcome and predictors required for our study.

| File | Dataset | Reason for inclusion |
|---|---|---|
| `P_DEMO.xpt` | Demographics | Provides age, sex, race/ethnicity, participant ID (`SEQN`), and survey information. |
| `P_BMX.xpt` | Body Measures | Provides BMI and waist circumference, key measures of body composition and metabolic health. |
| `P_BPXO.xpt` | Blood Pressure | Provides blood pressure measurements used as metabolic/clinical predictors. |
| `P_LUX.xpt` | Liver Ultrasound Transient Elastography | Provides Controlled Attenuation Parameter (CAP), which will be used to define the hepatic steatosis outcome. |
| `P_HDL.xpt` | HDL Cholesterol | Provides HDL cholesterol, a routinely measured marker of metabolic health. |
| `P_TRIGLY.xpt` | Triglycerides | Provides triglyceride levels, another important metabolic marker. |
| `P_GLU.xpt` | Plasma Fasting Glucose | Provides fasting blood glucose as a measure of glucose metabolism. |
| `P_DIQ.xpt` | Diabetes Questionnaire | Provides information about diabetes status/history. |

### Why these datasets?

The project focuses on whether **routinely available demographic, anthropometric, and metabolic variables** can identify hepatic steatosis.

Therefore, we selected datasets containing:

- Demographics: age, sex, race/ethnicity
- Anthropometrics: BMI and waist circumference
- Clinical measurements: blood pressure and diabetes status
- Laboratory measurements: HDL, triglycerides, and glucose
- Outcome: liver CAP measurement for defining hepatic steatosis

The datasets are merged using the NHANES participant identifier **`SEQN`**.

Other NHANES datasets are not currently included because they do not contain variables required for the initial research question.

## Analysis Workflow

The analysis is organized into a small number of notebooks, with each notebook representing one stage of the project.

```text
notebooks/
├── 01-data-preparation.ipynb
├── 02-metabolic-phenotyping.ipynb
├── 03-predictive-modeling.ipynb
├── 04-evaluation-interpretation.ipynb
└── 05-temporal-validation.ipynb       # Optional
```

### 1. Data Preparation (`01-data-preparation.ipynb`)

**Raw XPT files → select variables → rename variables → merge on `SEQN` → filter adults → require valid elastography and CAP → restrict to fasting subsample → remove incomplete predictor records → define hepatic steatosis from CAP → save analysis cohort**

Loads and merges the required NHANES 2017–March 2020 datasets, applies the study eligibility criteria, cleans the selected variables, and constructs the final analysis cohort. Hepatic steatosis is defined from the CAP measurement, and the resulting dataset is saved to `data/processed/analysis_cohort.csv`.

### 2. Metabolic Phenotyping (`02-metabolic-phenotyping.ipynb`)

**Load analysis cohort → train/test split → explore training metabolic variables → fit standardization on training data → determine number of clusters using training data → fit clustering on training data → characterize metabolic phenotypes → assign training and test participants to learned phenotypes → save split datasets**

The analysis cohort is first divided into training and test sets. Metabolic phenotypes are then identified using only the training data to prevent information from the held-out test set influencing phenotype discovery. BMI, waist circumference, blood pressure, HDL, triglycerides, and glucose are standardized and clustered within the training set. The fitted training-set scaler and K-means model are subsequently used to assign test participants to the learned phenotypes without refitting.

### 3. Predictive Modeling (`03-predictive-modeling.ipynb`)

**Load clustered train/test datasets → prepare predictors → logistic regression baseline → XGBoost without cluster ID → XGBoost with cluster ID → generate predictions**

Develops models for identifying hepatic steatosis from demographic, clinical, and metabolic predictors. Logistic regression provides a simple baseline, while the two XGBoost models allow assessment of whether metabolic phenotype information adds useful predictive information.

### 4. Evaluation and Interpretation (`04-evaluation-interpretation.ipynb`)

**Load model predictions → calculate performance metrics → compare models → evaluate performance by phenotype → calculate SHAP values → compare important predictors across phenotypes**

Evaluates model performance using metrics such as AUROC, AUPRC, sensitivity, and specificity. SHAP is then used to examine which variables contribute most strongly to XGBoost predictions overall and within each metabolic phenotype.

### 5. Temporal Validation (`05-temporal-validation.ipynb`, Optional)

**Prepare NHANES 2021–2023 data → harmonize variables → apply existing pipeline → generate predictions → evaluate performance → compare with 2017–2020 results**

Uses the newer NHANES 2021–2023 cycle as a temporal validation dataset to assess whether the developed approach and findings remain applicable in a more recent population.

## Overall Pipeline

```text
Raw NHANES data
→ Data preparation
→ Final analysis cohort
→ Train/test split
→ Training-set metabolic phenotyping
→ Assign test participants to learned phenotypes
→ Logistic regression + XGBoost
→ Model evaluation
→ SHAP and phenotype-specific interpretation
→ Optional 2021–2023 temporal validation
```