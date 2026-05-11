from web_search import search_candidate
from jd_scorer import score_candidate
from db_tool import insert_candidate, get_all, get_top3, get_by_name, delete_candidate

def web_search(query):
    return search_candidate(query)

def jd_scorer(summary, skills=None):

    if not summary or summary.strip() == "":
        return {
            "score": 40,   # ✅ default mid score
            "strengths": [],
            "gaps": ["No detailed profile found"]
        }

    summary = summary.lower()

    score = 0
    strengths = []
    gaps = []

    # ✅ smarter keyword groups
    skill_map = {
        "python": ["python", "py"],
        "machine learning": ["machine learning", "ml"],
        "sql": ["sql", "database"],
        "backend": ["backend", "api", "server", "flask", "django"]
    }

    for skill, keywords in skill_map.items():
        if any(k in summary for k in keywords):
            score += 20
            strengths.append(skill)
        else:
            gaps.append(f"Missing {skill}")


    if skills:
        for skill in skills:
            if skill in summary:
                score += 10
                strengths.append(skill)
            else:
                gaps.append(f"Lacks {skill}")

    
    if score == 0:
        score = 35   

    return {
        "score": min(score, 100),
        "strengths": strengths,
        "gaps": gaps
    }

def db_tool(action, data=None):

    if action == "INSERT":
        return insert_candidate(data)

    elif action == "SELECT":
        return get_by_name(data["name"])

    elif action == "LIST":
        return get_all()

    elif action == "TOP":
        return get_top3()

    elif action == "DELETE":
        return delete_candidate(data["name"])

    return "Invalid DB action"