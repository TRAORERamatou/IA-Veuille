from supabase_db.client import client_con


def get_active_sources():
    try:
        response = client_con.table("sources").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        print("Failed to fetch sources:", e)
        return []

#
def save_article(article_data: dict):
    try:
        response = client_con.table("articles").insert(article_data).execute()
        return response
    except Exception as e:
        print(" Error while saving:", e)
        return None

def article_exists(url: str) -> bool:
    try:
        response = client_con.table("articles").select("id").eq("url", url).limit(1).execute()
        return len(response.data) > 0
    except Exception as e:
        print("Error checking item :", e)
        return False
