
# 🌍 Country-State-City Category Scraper (Flask + MongoDB)

A web scraping utility panel built using **Flask** and **MongoDB**. It lets users:
- 📍 Scrape all cities of a selected country
- 🧾 Scrape structured location data by country → states → cities → categories
- 📥 Download the scraped city list as a `.csv` file

---

## 📦 Features

- **Two scraping modes:**
  - **Scrap Cities**: Fetch cities for a selected country.
  - **Scrap Details**: Choose country, states, and categories to store structured data in MongoDB.

- **Dynamic search** + **select all/reset all** on checkboxes
- Download scraped cities data as CSV
- Organized using BEM-style CSS and simple JS (no jQuery)

---

## 🚀 Tech Stack

- **Frontend**: HTML, Vanilla JS
- **Backend**: Python Flask
- **Database**: MongoDB
- **External APIs**: [countriesnow.space](https://countriesnow.space/api/v0.1)

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/mugesh-2104/flask-location-scraper.git
cd flask-location-scraper
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask pymongo requests
```

### 4. Start MongoDB

Ensure your local MongoDB server is running on:

```
mongodb://localhost:27017/
```

### 5. Run the Flask app

```bash
python app.py
```

Visit: `http://127.0.0.1:5000/` in your browser.

---

## 📂 Folder Structure

```
.
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── categories.json
└── README.md
```

---

## 🧪 Example MongoDB Record

```json
{
  "id": "b2f8381c-874e-4f18-8a5c-5cd8d0e7cc0f",
  "country": "India",
  "data": [
    {
      "state": "Tamil Nadu",
      "cities": ["Chennai", "Coimbatore", "Madurai"],
      "categories": ["cafe", "temple", "salon"]
    }
  ]
}
```

---

## 📌 Notes

- Ensure `categories.json` is in the `static/` folder and structured like:
```json
[
  { "categories": "restaurant" },
  { "categories": "salon" },
  { "categories": "hospital" }
]
```

- This project uses the public API from [countriesnow.space](https://countriesnow.space/), which may have rate limits or downtime.

---

## 📄 License

MIT License © Mugesh Kannan
