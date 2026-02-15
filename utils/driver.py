import undetected_chromedriver as uc
import random

def create_chrome_driver(headless=True):
    options = uc.ChromeOptions()
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    if headless:
        options.add_argument('--headless=new') 
    
    try:
        driver = uc.Chrome(
            options=options,
            version_main=145, 
            use_subprocess=True
        )
        
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
        return driver
    except Exception as e:
        print(f"Driver Error: {e}")
        raise