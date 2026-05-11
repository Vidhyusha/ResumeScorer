from tavily import TavilyClient
from config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def search_candidate(candidate_name):
    try:
        query = f"{candidate_name} software developer LinkedIn GitHub profile"

        response = client.search(query=query, search_depth="advanced")

        if response and "results" in response and len(response["results"]) > 0:

            results = response["results"]

            # ✅ prioritize LinkedIn / GitHub
            priority_links = [
                r for r in results
                if "linkedin.com" in r["url"] or "github.com" in r["url"]
            ]

            selected = priority_links[0] if priority_links else results[0]

            content = selected["content"][:1500] 
            link = selected["url"]

            return {
                "name": candidate_name,
                "summary": content,
                "links": [link]
            }

    except Exception as e:
        print("Search Error:", e)

    return {
        "name": candidate_name,
        "summary": "",
        "links": []
    }