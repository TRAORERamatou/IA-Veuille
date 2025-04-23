import scrapy
from datetime import datetime, timedelta

from ia_scraper.ia_scraper.items import IaScraperItem
from supabase_db.db_services import get_active_sources, article_exists, save_article
from supabase_db.summarizer import summarize_text


def safe_iso(dt):
    return dt.isoformat() if isinstance(dt, datetime) else None


class SmartAISpider(scrapy.Spider):
    name = "smart_ai"

    # def start_requests(self):
    #     sources = get_active_sources()
    #     for source in sources:
    #         if not source["active"]:
    #             continue
    #         yield scrapy.Request(
    #             url=source["url"],
    #             callback=self.parse_article_list,
    #             meta={
    #                 "source_name": source["name"],
    #                 "domain": source.get("domain", "undefined"),
    #                 "article_link_xpath": source.get("article_link_xpath", ""),
    #                 "content_xpath": source.get("content_xpath", ""),
    #                 "playwright": True
    #             }
    #         )

    def guess_article_links(self, response):
        self.logger.info("fallback mode: heuristic search for article links.")
        candidates = response.xpath("//a[not(contains(@href, '#')) and contains(@href, '/')]/@href").getall()
        full_links = [response.urljoin(link) for link in candidates if link.startswith("/")]
        return list(set(full_links))[:10]

    def parse_article_list(self, response):
        self.logger.info(f" Reading articles on : {response.url}")
        xpath = response.meta["article_link_xpath"]
        links = response.xpath(xpath).getall()[:5] if xpath else []

        if not links:
            self.logger.warning(f"No link found with XPath: {xpath} sur {response.url}")
            links = self.guess_article_links(response)

        for link in links:
            if link.endswith(('.jpg', '.png', '.jpeg')):
                continue
            full_url = response.urljoin(link)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_article,
                meta={
                    "source_name": response.meta["source_name"],
                    "domain": response.meta["domain"],
                    "content_xpath": response.meta["content_xpath"],
                    "playwright": True
                }
            )

    def guess_article_content(self, response):
        self.logger.info("Fallback mode: heuristic extraction of content")
        raw_text = response.xpath("//article//p/text() | //div[contains(@class, 'content') or contains(@class, 'body')]//p/text()").getall()
        return " ".join(raw_text).strip()

    def parse_article(self, response):
        url = response.url
        title = response.xpath('//title/text()').get(default="(Sans titre)").strip()
        content_xpath = response.meta["content_xpath"]
        paragraphs = response.xpath(content_xpath).getall() if content_xpath else []

        raw_text = " ".join(paragraphs).strip()
        if not raw_text or len(raw_text) < 100:
            raw_text = self.guess_article_content(response)

        if len(raw_text) < 100:
            self.logger.warning(f" Content always too short, ignored : {url}")
            return

        published_at = None
        date_str = response.xpath('//time/@datetime').get()
        if date_str:
            try:
                published_at = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                if published_at < datetime.utcnow() - timedelta(hours=1):
                    self.logger.info(f" Article too old (>{published_at}), ignored : {url}")
                    return
            except Exception:
                self.logger.warning(f" Unrecognized date format for: {url}")

        if article_exists(url):
            self.logger.info(f" Article already in the database : {url}")
            return

        summary = summarize_text(raw_text)

        article_data = {
            "title": title,
            "url": url,
            "source": response.meta["source_name"],
            "domain": response.meta["domain"],
            "published_at": safe_iso(published_at),
            "summary": summary
        }

        self.logger.info(f"Item to register: {title}")
        save_article(article_data)
        yield IaScraperItem(**article_data)
