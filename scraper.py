import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_cfr_news():
    base_url = "https://www.cfr.org"
    archive_url = f"{base_url}/newsletters/daily-news-brief"
    
    response = requests.get(archive_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all('a', href=True)
    article_link = None
    for link in links:
        href = link['href']
        if '/newsletters/' in href and href != '/newsletters/daily-news-brief':
            article_link = href if href.startswith('http') else base_url + href
            break
            
    if not article_link:
        print("Could not find the latest news link.")
        return

    article_response = requests.get(article_link)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    
    content_html = ""
    for element in article_soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        text = element.get_text(strip=True)
        if text:
            content_html += f"<{element.name}>{text}</{element.name}>\n"
            
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <title>CFR Daily</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 20px; max-width: 800px; margin: auto; line-height: 1.6; }}
        h1 {{ font-size: 1.5em; border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
        a {{ color: #0066cc; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>CFR Daily News - {date_str}</h1>
    <p><a href="{article_link}" target="_blank">View Original Source</a></p>
    <div>
        {content_html}
    </div>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    scrape_cfr_news()
