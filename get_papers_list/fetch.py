
import requests
import xml.etree.ElementTree as ET
import re

def is_non_academic(text):
    academic_keywords = ["university", "college", "institute", "school", "hospital", "lab"]
    return not any(word.lower() in text.lower() for word in academic_keywords)

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else "N/A"

def get_pubmed_ids(query, max_results=20):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results}
    r = requests.get(url, params=params)
    return r.json()["esearchresult"]["idlist"]

def fetch_details(pubmed_ids):
    if not pubmed_ids:
        return []

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    r = requests.get(url, params=params)
    root = ET.fromstring(r.content)

    papers = []

    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="N/A")
        pubmed_id = article.findtext(".//PMID", default="N/A")

        date = article.find(".//PubDate")
        pub_date = "-".join([
            date.findtext("Year", "N/A"),
            date.findtext("Month", "01"),
            date.findtext("Day", "01")
        ]) if date is not None else "N/A"

        authors = article.findall(".//Author")
        non_acad_authors = []
        affiliations = set()
        email = "N/A"

        for author in authors:
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
            for aff in author.findall(".//Affiliation"):
                aff_text = aff.text or ""
                if is_non_academic(aff_text):
                    non_acad_authors.append(name)
                    affiliations.add(aff_text)
                    if "@" in aff_text and email == "N/A":
                        email = extract_email(aff_text)

        if non_acad_authors:
            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_acad_authors),
                "Company Affiliation(s)": "; ".join(affiliations),
                "Corresponding Author Email": email,
            })

    return papers
