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