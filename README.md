#  Ai_Veille — Scraping des actualités IA
## Technologiy used

- [Scrapy]  (https://scrapy.org/)
- [Playwright]  (https://playwright.dev/)
- [Supabase]  (https://supabase.com/)
- [Google Gemini API]  (https://ai.google.dev/)
- [Python 3.13+]  (https://www.python.org/)
- [dotenv]  (https://pypi.org/project/python-dotenv/)

## main structure

Ai_Veille/ 
├── main.py # Manual scraper launch
├── auto_runner.py #Automated launch
├── ia_scraper/ #Scrapy project 
  ├── spiders/articles.py # Main Spider
  └── settings.py # Configs Scrapy & Playwright
├── supabase_db/ # Supabase connection
   ├── db_services.py │
   ├── summarizer.py #Summaries via Gemini 
   └── client.py ├── .env # Environment variables (not versioned)
├── requirements.txt └── README.md


### 1.  Clone the project
-cd ai_veille

### 2. Install dependencies

-python -m venv .venv
-source .venv/Scripts/activate    # Windows
# ou
source .venv/bin/activate        # Linux/macOS

### 3.Install required packages

-pip install -r requirements.txt

### 4. Configure the environment

-Crée un fichier .env et ajoute tes clés Supabase + Gemini :

-SUPABASE_URL=...
-SUPABASE_KEY=...
-GEMINI_API_KEY=...

### 5. Run the scraper
python main.py


