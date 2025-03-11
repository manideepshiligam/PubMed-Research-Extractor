# PubMed Research Paper Fetcher

## 📌 Overview
This script fetches research papers from PubMed based on a user-defined query. It extracts paper details such as:
- **Title**
- **Publication Date**
- **Non-Academic Authors**
- **Company Affiliations**
- **Corresponding Author Email**

The extracted data can be displayed in the terminal or saved as a **CSV file** for further analysis.

---

## 🚀 Features
- Fetches research papers from **PubMed API**.
- Extracts relevant details (title, authors, affiliations, etc.).
- **Filters out academic affiliations**, identifying company-based researchers.
- Saves results to **CSV format**.
- Includes a **debug mode** for better visibility.
- Allows users to specify the **number of results**.

---

## 📥 Installation

### Prerequisites
Ensure you have **Python 3.x** installed. You also need to install the required dependencies:

```bash
pip install requests
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/pubmed-fetcher.git
cd pubmed-fetcher
```

---

## 🛠 Usage

### Basic Command
To fetch **10 research papers** related to a topic (e.g., "cancer treatment") and display them in the console:
```bash
python papers_fetcher.py "cancer treatment"
```

### Save Results to CSV
To fetch **20 papers** on "diabetes research" and save them to `diabetes_papers.csv`:
```bash
python papers_fetcher.py "diabetes research" -n 20 -f diabetes_papers.csv
```

### Enable Debug Mode
To view detailed API requests and processing logs:
```bash
python papers_fetcher.py "AI in medicine" -d
```

### Arguments Explained
| Argument | Description | Example |
|----------|-------------|---------|
| `query`  | Search term for PubMed | "machine learning in healthcare" |
| `-n` or `--num-results` | Number of results (default: 10) | `-n 20` |
| `-f` or `--file` | Save results to a CSV file | `-f results.csv` |
| `-d` or `--debug` | Enable debug mode for detailed logs | `-d` |

---

## 🔍 How It Works
1. The script **sends a search request** to PubMed API to retrieve relevant paper IDs.
2. It **fetches details** of each paper using their respective **PubMed ID**.
3. The script **extracts and filters author affiliations**, identifying those working in companies.
4. It **displays results** in the terminal or saves them in **CSV format**.

---

## 🛠 Functions Explained
### `fetch_pubmed_papers(query, max_results=10)`
- Searches PubMed for papers based on the user query.
- Returns a list of PubMed IDs.

### `fetch_paper_details(pubmed_id, base_url)`
- Fetches full details of a paper using its **PubMed ID**.
- Extracts **title, authors, affiliations, and emails**.

### `extract_authors_affiliations(root)`
- Identifies **non-academic authors** and their **company affiliations**.

### `is_company(affiliation)`
- Determines if an **affiliation belongs to a company** instead of a university.

### `extract_corresponding_email(root)`
- Extracts the **corresponding author's email** if available.

### `save_to_csv(papers, filename)`
- Saves the extracted data into a **CSV file**.

---

## 🛠 Debugging & Error Handling
- **Connection issues?** Try re-running the script after a few minutes.
- **API rate limits?** Reduce the number of requests (`-n` argument) or add delays.
- **Missing author details?** Some papers may lack full metadata in PubMed.

---

## 🤖 Future Improvements
- Implement **multi-threading** to speed up API calls.
- Improve **company detection heuristics** using NLP.
- Add **support for API authentication** to increase request limits.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🏆 Author
Developed by **[Manideeep Shiligam]**. Contributions are welcome!

For feedback or feature requests, contact: **manideepsiddula@gmail.com**

