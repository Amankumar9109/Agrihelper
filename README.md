# 🌱 AgriHelper

**Empowering Farmers with Smart Agriculture, Market Intelligence, and Modern Techniques**

AgriHelper is a Flask-powered web platform designed to revolutionize the agricultural ecosystem in India. It bridges the gap between traditional farming and modern technology by providing real-time APMC mandi crop prices, weather insights, modern sustainable farming guides, government policy directories, an agricultural marketplace, and a farmer community platform.

---

## 📌 Key Features

### 1. 📊 Market Insights & Analytics
- **Dynamic Cascading Filters:** Select `State` ➔ `District` ➔ `Market (Mandi)` ➔ `Commodity`.
- **Price Breakdown:** Real-time computation of **Modal Price**, **Minimum Price**, and **Maximum Price** (₹/Quintal).
- **Comparative Analysis:** Compare modal prices across different markets within the state and nationwide benchmarks.
- Powered by Pandas data processing over comprehensive agricultural market datasets.

### 2. 🚜 Modern Farming Techniques
Interactive, dedicated guides for high-efficiency and sustainable agricultural practices:
- **Drip Irrigation:** Water-efficient micro-irrigation systems.
- **Soil Health Management:** Nutrient balancing, pH monitoring, and fertility improvement.
- **Vertical Farming:** Space-efficient indoor growing systems.
- **Agricultural Drones:** Aerial crop monitoring and automated spraying.
- **Hydroponics:** Soil-less crop cultivation.
- **AI & Data Analytics:** Precision farming, crop health diagnosis, and yield prediction.

### 3. 📜 Government Schemes & Policies
Comprehensive guides explaining financial support, eligibility, and step-by-step application instructions:
- **PM-KISAN:** ₹6,000/year direct income transfer to farmers.
- **PMFBY:** Crop insurance protection against climate hazards and natural calamities.
- **Soil Health Card Scheme:** Soil testing reports and customized fertilizer recommendations.
- **eNAM (National Agriculture Market):** Unified national digital trading platform.
- **Kisan Credit Card (KCC):** Accessible credit for farm inputs and equipment.

### 4. ☀️ Weather Analytics
- Climate conditions and weather forecasting to assist farmers with sowing, irrigation, and harvesting decisions.

### 5. 🛒 AgriHelper Store
- Direct marketplace showcase for seeds, organic fertilizers, tools, and modern machinery.

### 6. 🤝 Farmer Community
- Knowledge-sharing forum where farmers and agricultural specialists can publish questions, discuss challenges, and share farming practices.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask, Pandas
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Tailwind CSS, FontAwesome
- **Data Source:** Static JSON dataset (`static/data/market_data.json`)
- **Execution Script:** Batch script (`run.bat`) for quick startup on Windows

---

## 📂 Project Structure

```text
agrihelper/
├── app.py                      # Flask backend routes, API endpoints, & data processing
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows startup batch script
├── static/
│   ├── data/
│   │   └── market_data.json    # Mandi commodity pricing dataset
│   ├── market.css / market.js  # Styling & AJAX logic for market filtering
│   ├── modern_farming.css      # Styling for farming technique modules
│   ├── policy.css / policy.js  # Styling & search filter for government schemes
│   ├── script.js               # Global UI scripts
│   ├── style.css               # Landing page styles
│   └── weather.js              # Weather widget scripts
└── templates/
    ├── index.html              # Landing page
    ├── market.html             # Market price checker & visualizer
    ├── modern_farming.html     # Modern farming hub
    ├── drip.html, soil.html... # Individual modern farming guides
    ├── policy.html             # Government policies directory
    ├── p1.html - p5.html       # Individual policy detail pages
    ├── weather.html            # Weather forecast page
    ├── store.html              # Agricultural store
    ├── community.html          # Farmer community discussion board
    ├── post.html               # Community post creation
    └── login.html              # Authentication page
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system.
- `pip` (Python package manager).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Amankumar9109/Agrihelper.git
   cd Agrihelper
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Application

### Option 1: Using the Python Launcher (Windows)
```powershell
py app.py
```

### Option 2: Standard Python command
```powershell
python app.py
```

### Option 3: Using the Windows Batch script
Double-click `run.bat` or run:
```powershell
.\run.bat
```

Once started, open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 💡 Troubleshooting

- **`ModuleNotFoundError: No module named 'flask'`:**
  If you have multiple Python versions installed (e.g. MinGW/MSYS2 in your `PATH`), make sure you run the app with the Python version where packages were installed:
  ```powershell
  py app.py
  ```
  Or check your active Python path:
  ```powershell
  where python
  py --list
  ```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve features, add new schemes, or optimize data processing:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
