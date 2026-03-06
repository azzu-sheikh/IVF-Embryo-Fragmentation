````markdown
<div align="center">

# 🧬 AI-Powered IVF Embryo Grading System

**A state-of-the-art computer vision pipeline and clinical dashboard for automating *in-vitro fertilization (IVF)* embryo quality assessment**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=PyTorch&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-yellow.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=OpenCV&logoColor=white)

</div>

---

# 🔬 The Clinical Problem

In modern IVF clinics, **embryo fragmentation assessment is performed manually** by embryologists.  
This process is **highly subjective** and leads to large inconsistencies in clinical evaluation.

Studies show **20–30% inter-observer variability** in embryo grading, which directly affects:

- Blastocyst development prediction
- Embryo selection accuracy
- Overall pregnancy success rates

A **standardized AI-based evaluation system** can dramatically improve reproducibility and decision-making in assisted reproduction.

Source:  
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6434759/

---

# 💡 The Solution

This project introduces an **AI-driven embryo analysis pipeline** that replaces subjective human estimates with **objective pixel-level mathematical analysis**.

Using a **custom-trained YOLOv8 Instance Segmentation model**, the system:

1. Detects embryo structures
2. Segments cellular fragments
3. Calculates fragmentation percentage
4. Generates standardized clinical grades

The result is a **fast, automated, and reproducible embryo grading workflow**.

---

# ✨ Key Features

### 🧠 Live AI Segmentation
Automatically detects and segments:

- **Embryo Body (Class 0)**
- **Cellular Fragments (Class 1)**

using a **custom YOLOv8-seg model**.

---

### 🧮 Advanced Tensor Mathematics

A custom **PyTorch backend** merges segmentation masks using:

```python
torch.logical_or()
````

This ensures:

* overlapping pixels are merged
* double counting is eliminated
* true physical fragmentation area is calculated.

---

### 📊 Clinical Grading Logic

Embryos are automatically classified using clinical safety thresholds:

| Fragmentation | Grade       |
| ------------- | ----------- |
| < 10%         | 🟢 Good     |
| 10% – 25%     | 🟡 Moderate |
| > 25%         | 🔴 Bad      |

---

### 🎨 Modern Neumorphic Dashboard

A highly polished **Streamlit interface** featuring:

* 3D glassmorphic UI
* gradient controls
* dynamic **Dark 🌙 / Light ☀️ mode**
* responsive dashboard layout

---

### 📈 Interactive Visualization

Clinical scores are visualized with **Plotly gauge charts**, enabling intuitive interpretation of embryo quality.

---

### 📄 Automated Clinical Reporting

The system logs session data and allows clinicians to export:

* **CSV Reports** (Pandas)
* **Formatted PDF Reports** (FPDF)

for clinical documentation.

---

# 🛠️ Technology Stack

| Category          | Technologies                  |
| ----------------- | ----------------------------- |
| Deep Learning     | YOLOv8 (Ultralytics), PyTorch |
| Data Engineering  | Roboflow, Pandas, NumPy       |
| Computer Vision   | OpenCV, Pillow                |
| Frontend UI       | Streamlit, HTML/CSS           |
| Visualization     | Plotly                        |
| Training Hardware | Kaggle (Dual NVIDIA T4 GPUs)  |

Sources:
[https://ultralytics.com](https://ultralytics.com)
[https://pytorch.org](https://pytorch.org)
[https://streamlit.io](https://streamlit.io)

---

# 🏗️ System Architecture

### 1️⃣ Data Pipeline

Clinical **Day-3 embryo microscope images** were annotated using **Roboflow**.

Dataset expansion techniques:

* rotation
* flipping
* contrast augmentation
* scaling

Final dataset size:

**1500+ images**

---

### 2️⃣ Model Training

A **YOLOv8 Medium segmentation model** was trained for:

* **100 epochs**
* optimizer: **AdamW**
* metric: **mAP@50**

Source:
[https://docs.ultralytics.com](https://docs.ultralytics.com)

---

### 3️⃣ Inference Engine

During inference the system:

1. Predicts segmentation masks
2. Creates PyTorch tensors
3. Merges intersecting masks
4. Calculates fragmentation area
5. Generates clinical score

---

### 4️⃣ Web Application

The AI pipeline is deployed through a **Streamlit dashboard** for real-time embryo analysis.

---

# 🚀 Installation & Usage

## Prerequisites

* Python **3.9+**
* Virtual environment recommended

Source:
[https://docs.python.org/3/](https://docs.python.org/3/)

---

## Step 1 — Clone Repository

```bash
git clone https://github.com/azzu-sheikh/IVF-Embryo-Fragmentation.git
cd IVF-Embryo-Fragmentation
```

---

## Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

Example dependencies:

```
streamlit
ultralytics
torch
opencv-python-headless
pandas
plotly
pillow
fpdf
```

---

## Step 3 — Add Model Weights

Place your trained model:

```
best.pt
```

in the root directory:

```
IVF-Embryo-Fragmentation
 ├── app.py
 ├── best.pt
 ├── requirements.txt
```

---

## Step 4 — Run the Application

```bash
streamlit run app.py
```

The dashboard will open automatically at:

```
http://localhost:8501
```

Source:
[https://docs.streamlit.io/](https://docs.streamlit.io/)

---

# 👨‍💻 Author

### Abdul Azeem Sheikh

Information Science Engineer
AI & Data Science Enthusiast

Focused on building **machine learning systems for healthcare automation and real-world problem solving**.

🌐 Portfolio
[https://azeemsheikh.vercel.app/](https://azeemsheikh.vercel.app/)

📧 Email
[abdulazeemsheik4@gmail.com](mailto:abdulazeemsheik4@gmail.com)

💼 GitHub
[https://github.com/azzu-sheikh/IVF-Embryo-Fragmentation](https://github.com/azzu-sheikh/IVF-Embryo-Fragmentation)

---

# ⭐ Support the Project

If you found this project useful:

⭐ **Star the repository**
🍴 **Fork the project**
📢 **Share it with the community**

Contributions and feedback are always welcome.

---

```
```
