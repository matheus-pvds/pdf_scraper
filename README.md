# We — FGV Concurso PDF Scraper & Downloader

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-5B4638?logo=Python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A web scraper that crawls **FGV Conhecimento** (Fundação Getulio Vargas) public exam/contest pages, extracts all PDF links, downloads them, and catalogs them by contest.

## Features

- **Crawls FGV Concurso Pages** — predefined list of public exam URLs
- **PDF Link Extraction** — parses HTML for all PDF download links
- **Streaming Downloads** — downloads PDFs in 8KB chunks with skip-already-downloaded logic
- **Contest Organization** — organizes downloads into subdirectories per contest
- **Link Catalog** — saves all found PDF links to `links_pdfs_encontrados.txt`
- **User-Agent Spoofing** — avoids blocking with custom headers

## Tech Stack

Python, requests, BeautifulSoup 4, urllib.parse

## Architecture

Single-file script (`main.py`) with three functions:

- `extrair_links_pdf(url)` — fetches page, parses HTML, returns PDF links
- `baixar_pdf(url, caminho)` — streams PDF download to disk
- **Main block** — iterates 5 target URLs, creates subdirectories, downloads all PDFs

### Contest Directories

```
pdfs_concursos/
├── camaracaruaru/
├── cma20/
├── cms2017/
├── cmsp23/
├── cmsp23_consultor/
```

## Usage

```bash
pip install requests beautifulsoup4
python main.py
```

## License

MIT
