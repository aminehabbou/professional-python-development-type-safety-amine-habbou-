import io
import xml.etree.ElementTree as ET

import pandas as pd
import requests

url = "http://export.arxiv.org/api/query"


def fetch_arxiv_articles(query: str, i: int = 0) -> pd.DataFrame:
    params: dict[str, str | int] = {
        "search_query": f"all:{query}",
        "start": i,
        "max_results": 10,
    }
    response = requests.get(url, params=params)
    xml_data = response.text
    return load_from_xml(xml_data)


def load_from_xml(xml_data: str) -> pd.DataFrame:
    file_like = io.StringIO(xml_data)
    df = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )[["id", "title", "summary"]]
    df.rename(columns={"id": "arxiv_id"}, inplace=True)
    df["author_title"] = "PhD"

    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    pdf_links = []
    authors = []

    for entry in root.findall("atom:entry", ns):
        pdf = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf = link.attrib.get("href")
                break
        pdf_links.append(pdf or "N/A")
        author_elem = entry.find("atom:author/atom:name", ns)
        authors.append(author_elem.text if author_elem is not None else "Unknown")

    df["file_path"] = pdf_links
    df["author_full_name"] = authors

    return df
