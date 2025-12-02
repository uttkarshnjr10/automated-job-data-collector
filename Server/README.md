# Job Market ETL (Python Web Scraper + MySQL)

A simple ETL pipeline that scrapes remote Python job listings from **WeWorkRemotely**, 
extracts structured job data, and loads it into a MySQL database.

## 🚀 Features

- Extracts: **job title**, **company name**, **location**, **job link**
- Clean HTML parsing using **BeautifulSoup**
- Stores jobs safely in **MySQL**
- Prevents duplicates automatically
- Fully modular & easy to extend

---

## 📂 Project Structure

Job-Market-ETL/
│── scraper.py # Main ETL script (Extract → Parse → Load)
│── db_config.py # Local MySQL credentials (ignored in Git)
│── requirements.txt # Python dependencies
│── README.md
│── .gitignore
│── venv/ (ignored)