# 🚗 Boodmo Car Spare Parts Scraping Project

A **Scrapy-based web scraping project** to extract category links, product links, and detailed product data from **Boodmo.com**, an online marketplace for car spare parts and accessories in India.

---
# Important Notes

*Before Running a spider make sure to change header cookies 

---

## 📌 Project Overview

Boodmo is a platform where users can search, compare, and purchase OEM (original) and aftermarket spare parts.

This project automates the extraction of:

* Category data
* Product links
* Product details

---

## 🔄 Scraping Workflow

```text
Car Filter
   ↓
Category
   ↓
Product Links
   ↓
Product Data
```

---

## 🕷️ Spiders Description

### 1️⃣ `extract_category_link`

* Extracts all final category URLs
* Saves data into JSON

**Output:**

```
All_Category_Data.json
```

---

### 2️⃣ `extract_product_link`

* Uses category links
* Extracts all product URLs

**Input:**

```
All_Category_Data.json
```

**Output:**

```
All_Product_Link.json
```

---

### 3️⃣ `extract_product_data`

* Uses product links
* Extracts detailed product data

**Input:**

```
All_Product_Link.json
```

**Output:**

* JSON file
* Excel file

---


###  Install Requirements

```bash
pip install -r requirements.txt
```

If no requirements file:

```bash
pip install scrapy pandas openpyxl
```

---

## ▶️ How to Run (Execution Steps)

### Step 1: Extract Category Links

```bash
scrapy crawl extract_category_link
```

➡ Output: `All_Category_Data.json`

---

### Step 2: Extract Product Links

```bash
scrapy crawl extract_product_link
```

➡ Output: `All_Product_Link.json`

---

### Step 3: Extract Product Data

```bash
scrapy crawl extract_product_data
```

➡ Output:

* `product_data.json`
* `product_data.xlsx`

---

## 📁 Project Structure

```text
boodmo-scraper/
│
├── boodmo/
│   ├── spiders/
│   │   ├── extract_category_link.py
│   │   ├── extract_product_link.py
│   │   └── extract_product_data.py
│   │
│   ├── items.py
│   ├── pipelines.py
│   ├── middlewares.py
│   └── settings.py
│
├── output/
│   ├── All_Category_Data.json
│   ├── All_Product_Link.json
│   ├── product_data.json
│   └── product_data.xlsx
│
├── requirements.txt
├── scrapy.cfg
└── README.md
```

---

## 📊 Extracted Data Fields

Typical product data includes:

* Product Name
* Price
* Brand
* Category
* Subcategory
* Availability
* SKU / Part Number
* Description
* Image URL
* Delivery Info

---


## ⚠️ Important Notes

* Always run spiders **in sequence**
* Ensure input files exist before next step
* Configure headers/cookies if required
* Add delays or proxies if needed

---



---

## 👨‍💻 Author

**Niraj Chauhan**
Python Developer | Web Scraping Engineer




