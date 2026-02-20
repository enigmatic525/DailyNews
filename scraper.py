import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_cfr_news():
    base_url = "https://www.cfr.org"
    archive_url = f"{base_url}/newsletters/daily-news-brief"
    # Added User-Agent so the website doesn't block us for being a bot
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # Set default values so the file ALWAYS generates
    content_html = "<p>Could not fetch today's news. The script failed to find the latest article link.</p>"
    article_link = archive_url
    
    try:
        response = requests.get(archive_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            # Look for links containing daily-news-brief but not the main archive page
            if 'daily-news-brief' in href and href != '/newsletters/daily-news-brief' and not href.startswith('#'):
                article_link = href if href.startswith('http') else base_url + href
                break
                
        if article_link != archive_url:
            article_response = requests.get(article_link, headers=headers)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            content_html = ""
            for element in article_soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
                text = element.get_text(strip=True)
                if text:
                    content_html += f"<{element.name}>{text}</{element.name}>\n"
    except Exception as e:
        content_html = f"<p>An error occurred while scraping: {e}</p>"
            
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
    
    # This will now always run, preventing the GitHub Action from failing
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    scrape_cfr_news()
