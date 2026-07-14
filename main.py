import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Configuração de cabeçalho para evitar bloqueios do servidor
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extrair_links_pdf(url):
    print(f"\n[Mapeando] Acessando: {url}")
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=15)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"    [Erro] Falha ao acessar o site: {e}")
        return []

    soup = BeautifulSoup(resposta.text, 'html.parser')
    pdfs_encontrados = set()

    for tag_a in soup.find_all('a', href=True):
        href = tag_a['href'].strip()
        if not href or href.startswith('#'):
            continue
            
        url_completa = urljoin(url, href)
        url_limpa = urlparse(url_completa).path
        
        if url_limpa.lower().endswith('.pdf') or '.pdf' in href.lower():
            pdfs_encontrados.add(url_completa)

    return sorted(list(pdfs_encontrados))

def baixar_pdf(url_pdf, pasta_destino):
    # Extrai o nome do arquivo a partir da URL
    nome_arquivo = os.path.basename(urlparse(url_pdf).path)
    
    # Caso a URL termine de forma estranha, garante o nome correto
    if not nome_arquivo.lower().endswith('.pdf'):
        nome_arquivo += ".pdf"
        
    caminho_final = os.path.join(pasta_destino, nome_arquivo)
    
    # Se o arquivo já existe, pula para economizar banda e tempo
    if os.path.exists(caminho_final):
        print(f"    [Pulado] Já existe: {nome_arquivo}")
        return

    try:
        print(f"    [Baixando] {nome_arquivo}...", end="", flush=True)
        resposta = requests.get(url_pdf, headers=HEADERS, stream=True, timeout=30)
        resposta.raise_for_status()
        
        with open(caminho_final, 'wb') as f:
            for chunk in resposta.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(" OK!")
    except Exception as e:
        print(f" ERRO! (Falha no download: {e})")

# --- Execução Principal ---
if __name__ == "__main__":
    # Lista de sites fornecida
    sites = [
        "https://conhecimento.fgv.br/concursos/cma20",
        "https://conhecimento.fgv.br/concursos/cms2017",
        "https://conhecimento.fgv.br/concursos/camaracaruaru",
        "https://conhecimento.fgv.br/concursos/cmsp23/1",
        "https://conhecimento.fgv.br/concursos/cmsp23"
    ]
    
    # Cria a pasta raiz para salvar os downloads
    pasta_raiz_downloads = "pdfs_concursos"
    os.makedirs(pasta_raiz_downloads, exist_ok=True)
    
    ARQUIVO_TXT = "links_pdfs_encontrados.txt"
    
    # Abre o arquivo TXT para escrita limpa (sobrescreve se já existir)
    with open(ARQUIVO_TXT, "w", encoding="utf-8") as txt:
        txt.write("=== LINKS DE PDFS EXTRAÍDOS ===\n\n")
    
    # Processa site por site
    for url_site in sites:
        links_pdf = extrair_links_pdf(url_site)
        total = len(links_pdf)
        print(f"    -> Encontrados {total} PDFs.")
        
        if total == 0:
            continue
            
        # 1. Salva a lista no arquivo TXT
        with open(ARQUIVO_TXT, "a", encoding="utf-8") as txt:
            txt.write(f"Site Origem: {url_site}\n")
            txt.write(f"Quantidade: {total}\n")
            for link in links_pdf:
                txt.write(f"{link}\n")
            txt.write("-" * 80 + "\n\n")
            
        # 2. Cria subpasta específica para este concurso
        # Pega a última parte da URL como nome da pasta (ex: cma20, cmsp23)
        nome_pasta_concurso = url_site.rstrip('/').split('/')[-1]
        # Tratamento especial para a subpágina '1' da cmsp23 para não virar uma pasta chamada '1'
        if nome_pasta_concurso == '1':
            nome_pasta_concurso = "cmsp23_consultor"
            
        pasta_destino_concurso = os.path.join(pasta_raiz_downloads, nome_pasta_concurso)
        os.makedirs(pasta_destino_concurso, exist_ok=True)
        
        # 3. Faz o download de cada PDF mapeado
        for link in links_pdf:
            baixar_pdf(link, pasta_destino_concurso)
            
    print(f"\n======== PROCESSO CONCLUÍDO ========")
    print(f"-> O arquivo com a lista de links foi gerado em: '{ARQUIVO_TXT}'")
    print(f"-> Os arquivos baixados estão organizados na pasta: '{pasta_raiz_downloads}/'")