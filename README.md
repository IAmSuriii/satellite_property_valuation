#  Satellite Property Valuation

A multimodal machine learning project that predicts residential property prices by combining structured tabular data with satellite imagery. The project demonstrates how environmental and spatial context extracted from satellite images can enhance traditional real-estate valuation models.

---

## Limitations

Due to satellite image download constraints and API usage limits, satellite imagery was collected for a subset of the dataset. As a result, the multimodal model was trained and evaluated only on properties with available images. Specifically, images were downloaded for approximately **3,000 properties** in both the training and test sets. Consequently, the final `24114073_final.csv` contains predictions only for these corresponding property IDs.

---

##  Project Overview

Traditional property valuation models rely primarily on tabular attributes such as size, location, and neighborhood statistics. This project extends that approach by integrating satellite imagery, enabling the model to capture visual environmental cues such as surrounding land use, green cover, road density, and proximity to water.

A multimodal regression pipeline is developed using:

- A **Convolutional Neural Network (CNN)** to extract visual embeddings from satellite images  
- A **Multilayer Perceptron (MLP)** to process tabular housing features  
- A **fusion mechanism** to jointly predict property prices  

The project compares a **tabular-only baseline** against a **tabular + satellite imagery model** and provides visual explainability using **Grad-CAM**.

---

##  Project Structure
```
satellite_property_valuation/
│
├── data/
│ ├── train.xlsx
│ └── test2.xlsx
│
├── images/
│ ├── train/
│ └── test/
│
├── img_extract.ipynb
├── data_fetcher.py
├── preprocessing.ipynb
├── model_training.ipynb
├── submission.csv
├── figures/
│ └── architecture_diagram.png
└── README.md
```

---

## Dataset Description

### Tabular Data

The base dataset contains housing attributes such as:

- `price` (target variable)
- `bedrooms`, `bathrooms`
- `sqft_living`, `sqft_above`, `sqft_basement`
- `sqft_lot`, `sqft_living15`, `sqft_lot15`
- `condition`, `grade`, `view`, `waterfront`
- `lat`, `long`

### Satellite Imagery

Satellite images are fetched programmatically using latitude and longitude coordinates. Each image represents a localized region around a property and provides environmental context not explicitly captured by tabular features.

---

##  How to Run the Project

Follow the steps below **in order**.

### Step 1: Prepare Data

Place the Excel files inside the `data/` directory:

data/train.xlsx
data/test2.xlsx


---

### Step 2: Generate CSV Files

Run:

img_extract.ipynb

yaml
Copy code

This notebook:
- Reads the Excel files
- Extracts required columns (`id`, `lat`, `long`)
- Generates:
  - `train.csv`
  - `test.csv`

---

### Step 3: Download Satellite Images

Run:

python data_fetcher.py


This script:
- Uses the Sentinel Hub API
- Downloads satellite images using coordinates from CSV files
- Saves images to:

images/train/
images/test/


---

### Step 4: Preprocessing & EDA

Run:

preprocessing.ipynb


This notebook performs:
- Data cleaning and filtering
- Log transformation of the target variable
- Exploratory and geospatial data analysis
- Feature scaling
- Dataset preparation for modeling

---

### Step 5: Model Training & Prediction

Run:

model_training.ipynb


This notebook:
- Trains a **tabular-only baseline model**
- Trains a **multimodal model (CNN + MLP)**
- Evaluates models using **RMSE** and **R²**
- Generates **Grad-CAM visualizations**
- Produces final predictions

Final output:

submission.csv


Format:

id,predicted_price


---

## Results Summary

| Model | RMSE ↓ | R² ↑ |
|------|--------|------|
| Tabular Only | ~0.305 | ~0.673 |
| Tabular + Satellite Images | **~0.250** | **~0.774** |

The multimodal model consistently outperforms the tabular-only baseline, demonstrating the benefit of incorporating satellite imagery.

---

##  Model Explainability

Grad-CAM is used to visualize which regions of satellite images influence the model’s predictions. The CNN focuses on spatially coherent regions, indicating that environmental context plays a meaningful role in price estimation.

---

##  Tech Stack

- **Data Handling:** Pandas, NumPy  
- **Deep Learning:** PyTorch  
- **Image Processing:** PIL  
- **Machine Learning:** Scikit-learn  
- **Visualization:** Matplotlib  
- **Explainability:** Grad-CAM  
- **Satellite Data:** Sentinel Hub API  

---

##  Key Takeaway

This project demonstrates that **multimodal learning**, combining tabular data with satellite imagery, can s