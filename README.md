# NHANES Hepatic Steatosis Screening

This project uses NHANES data to investigate whether routinely available demographic and metabolic variables can identify adults with hepatic steatosis.

The analysis uses the **NHANES 2017–March 2020 pre-pandemic dataset**.

## Project Structure

```text
nhanes-steatosis/
├── data/
│   ├── raw/
│   │   └── 2017-2020/       # Original NHANES XPT files
│   ├── processed/           # Cleaned and transformed datasets
│   └── models/              # Fitted pipelines and selected parameters
├── notebooks/               # Analysis notebooks
├── src/                     # Downloading and processing scripts
├── results/                 # Tuning results
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
├── 03-model-development.ipynb
└── 04-evaluation-interpretation.ipynb
```

### 1. Data Preparation (`01-data-preparation.ipynb`)

**Raw XPT files → select variables → rename variables → merge on `SEQN` → filter adults → require valid elastography and CAP → restrict to fasting subsample → remove incomplete predictor records → define hepatic steatosis from CAP → save analysis cohort**

Loads and merges the required NHANES 2017–March 2020 datasets, applies the study eligibility criteria, cleans the selected variables, and constructs the final analysis cohort. Hepatic steatosis is defined from the CAP measurement, and the resulting dataset is saved to `data/processed/analysis_cohort.csv`.

### 2. Metabolic Phenotyping (`02-metabolic-phenotyping.ipynb`)

**Load analysis cohort → train/test split → explore training metabolic variables → fit standardization on training data → determine number of clusters using training data → fit clustering on training data → characterize metabolic phenotypes → assign training and test participants to learned phenotypes → save split datasets**

The analysis cohort is first divided into training and test sets. Metabolic phenotypes are then identified using only the training data to prevent information from the held-out test set influencing phenotype discovery. BMI, waist circumference, blood pressure, HDL, triglycerides, and glucose are standardized and clustered within the training set. The fitted training-set scaler and K-means model are subsequently used to assign test participants to the learned phenotypes without refitting.

### 3. Model Development (`03-model-development.ipynb`)

**Load phenotyped training cohort → prepare predictors and preprocessing pipelines → fit logistic regression baseline → tune XGBoost without phenotype using five-fold stratified cross-validation → retain selected base model → fit XGBoost with phenotype using the same selected hyperparameters → save fitted pipelines and tuning results**

Develops three models using only the training cohort: logistic regression, XGBoost without metabolic phenotype and XGBoost with metabolic phenotype. XGBoost hyperparameters are selected using five-fold stratified cross-validation, with mean validation AUROC as the selection criterion. The selected configuration is used for both XGBoost models, and all fitted pipelines are saved for held-out evaluation.

### 4. Evaluation and Interpretation (`04-evaluation-interpretation.ipynb`)

**Load fitted models and held-out test cohort → generate test predictions once → calculate overall performance metrics → evaluate performance by metabolic phenotype → visualize ROC/PR curves and classification errors → quantify AUROC uncertainty and model differences → calculate overall and phenotype-specific SHAP values → interpret findings**

Loads the three fitted model pipelines and generates predictions once for the held-out test cohort. Overall performance is evaluated using AUROC, AUPRC, sensitivity, specificity and other relevant metrics. The models are compared to assess whether XGBoost improves on logistic regression and whether explicitly adding metabolic phenotype improves XGBoost performance. Performance is then examined separately within each metabolic phenotype. Bootstrap confidence intervals and paired model comparisons quantify uncertainty in AUROC estimates, while SHAP is used to examine predictor contributions overall and within each metabolic phenotype.

## Overall Pipeline

```text
Raw NHANES data
→ Data preparation
→ Final analysis cohort
→ Train/test split
→ Training-set metabolic phenotyping
→ Assign test participants to learned phenotypes
→ Logistic regression baseline
→ XGBoost tuning and model development
→ Held-out model evaluation
→ Phenotype-specific evaluation
→ SHAP interpretation
```