
import argparse
import csv
from get_papers_list.fetch import get_pubmed_ids, fetch_details

def main():
    parser = argparse.ArgumentParser(description="Fetch pharma/biotech research papers from PubMed")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output file to save results as CSV")
    parser.add_argument("-d", "--debug", action="store_true", help="Show debug info")

    args = parser.parse_args()

    if args.debug:
        print("Searching for:", args.query)

    ids = get_pubmed_ids(args.query)
    if args.debug:
        print("Found PubMed IDs:", ids)

    papers = fetch_details(ids)

    if args.file:
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        print("Saved to:", args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
