import requests
import xml.etree.ElementTree as ET
import argparse
import csv
import time
from typing import List, Dict, Tuple, Optional

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_papers(query: str, max_results: int = 10, debug: bool = False) -> List[Dict[str, str]]:
    """
    Fetch research papers from PubMed based on a search query.
    
    :param query: The search query.
    :param max_results: Number of results to fetch.
    :param debug: Print debug information if True.   
    :return: List of dictionaries with paper details.
    """
    search_url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        search_results = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching search results: {e}")
        return []

    pubmed_ids = search_results.get("esearchresult", {}).get("idlist", [])
    if debug:
        print(f"🔍 Found {len(pubmed_ids)} papers for query: {query}")
    
    papers = []
    for pubmed_id in pubmed_ids:
        details = fetch_paper_details(pubmed_id, debug)
        if details:
            papers.append(details)
        time.sleep(0.5)  # Avoid hitting API rate limits

    return papers

def fetch_paper_details(pubmed_id: str, debug: bool = False) -> Optional[Dict[str, str]]:
    """
    Fetch details of a research paper using its PubMed ID.
    
    :param pubmed_id: The PubMed ID of the paper.
    :param debug: Print debug information if True.
    :return: Dictionary containing the paper details.
    """
    fetch_url = f"{BASE_URL}efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    
    try:
        response = requests.get(fetch_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching paper {pubmed_id}: {e}")
        return None

    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    
    title = root.findtext(".//ArticleTitle", "N/A")
    publication_date = root.findtext(".//PubDate/Year", "N/A")
    authors, companies = extract_authors_affiliations(root)
    corresponding_email = extract_corresponding_email(root)

    if debug:
        print(f"✅ Processed {pubmed_id}: {title}")

    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": publication_date,
        "Non-academic Author(s)": ", ".join(authors) if authors else "N/A",
        "Company Affiliation(s)": ", ".join(companies) if companies else "N/A",
        "Corresponding Author Email": corresponding_email or "N/A"
    }

def extract_authors_affiliations(root: ET.Element) -> Tuple[List[str], List[str]]:
    """
    Extract authors and company affiliations from the XML tree.
    
    :param root: XML root element.
    :return: Tuple containing lists of non-academic authors and their companies.
    """
    authors = []
    companies = []
    
    for author in root.findall(".//Author"):
        first_name = author.findtext("ForeName", "").strip()
        last_name = author.findtext("LastName", "").strip()
        name = f"{first_name} {last_name}".strip()
        affiliation = author.findtext(".//Affiliation", "").strip()
        
        if name and affiliation and is_company(affiliation):
            authors.append(name)
            companies.append(affiliation)
    
    return authors, companies

def is_company(affiliation: str) -> bool:
    """
    Determine if an affiliation belongs to a company.
    
    :param affiliation: Affiliation text.
    :return: True if it's a company, False otherwise.
    """
    academic_keywords = ["University", "Institute", "College", "School", "Hospital", "Academy", "Center"]
    return not any(keyword.lower() in affiliation.lower() for keyword in academic_keywords)

def extract_corresponding_email(root: ET.Element) -> Optional[str]:
    """
    Extract the email of the corresponding author if available.
    
    :param root: XML root element.
    :return: The corresponding author's email, if found.
    """
    for email in root.findall(".//ElectronicAddress"):
        return email.text
    return None

def save_to_csv(papers: List[Dict[str, str]], filename: str):
    """
    Save paper details to a CSV file.
    
    :param papers: List of paper details.
    :param filename: CSV filename.
    """
    if not papers:
        print("⚠️ No data to save.")
        return
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"📁 Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-n", "--num-results", type=int, default=10, help="Number of results to fetch (default: 10)")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")

    args = parser.parse_args()

    if args.debug:
        print(f"🔍 Querying PubMed for: {args.query} (Max results: {args.num_results})")

    papers = fetch_pubmed_papers(args.query, max_results=args.num_results, debug=args.debug)

    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
