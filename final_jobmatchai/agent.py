from tools import web_search, jd_scorer
from db_tool import insert_candidate, delete_candidate, get_all, get_top3, get_by_name

MAX_ITERATIONS = 8


# ===============================
# DECISION LOGIC
# ===============================
def decide(score, summary, has_profile=True, role_match=True):

    if not has_profile:
        return "Insufficient Info — Request Resume"


    if score >= 75:
        return "Recommend: Interview"
    
    if 30 <= score <= 55:
        return "Insufficient Info — Request Resume"

    if score < 30:
        return "Reject"

    if not role_match and score < 60:
        return "Insufficient Info — Request Resume"

    return "Consider"

def run_agent(command):

    cmd = command.lower()

    # ===============================
    # DB COMMANDS
    # ===============================
    if "all" in cmd and "candidate" in cmd:
        print("Thought: User wants all candidates.")
        print("Observation:", get_all())
        return

    if "top" in cmd:
        print("Thought: User wants top candidates.")
        print("Observation:", get_top3())
        return

    if "delete" in cmd or "remove" in cmd:
        name = command.replace("delete", "").replace("remove", "").strip().lower()
        print("Thought: Deleting candidate...")
        print("Observation:", delete_candidate(name))
        return

    # ===============================
    # STATE
    # ===============================
    state = {
        "candidate": "",
        "summary": "",
        "score": None,
        "strengths": [],
        "gaps": [],
        "profile_url": "",
        "has_profile": True,
        "role_match": True,
        "required_skills": [],
        "done": False
    }

    print("\n--- AGENT START ---")

    for step in range(MAX_ITERATIONS):

        print(f"\nIteration {step+1}")

        # ===============================
        # STEP 1: Extract candidate + skills
        # ===============================
        if not state["candidate"]:
            words = command.split()

            if "for" in words:
                name = " ".join(words[1:words.index("for")])
            else:
                name = " ".join(words[1:3])

            state["candidate"] = name.lower()

            # extract skills from command
            for skill in ["python", "backend", "flask", "django", "api"]:
                if skill in cmd:
                    state["required_skills"].append(skill)

            print(f"Candidate: {state['candidate']}")
            continue

        # ===============================
        # STEP 2: Web Search
        # ===============================
        if not state["summary"]:
            result = web_search(state["candidate"])
            print("Observation:", result)

            state["summary"] = result.get("summary", "")
            links = result.get("links", [])

            state["profile_url"] = links[0] if links else "N/A"
            state["has_profile"] = bool(links)

            continue

        # ===============================
        # STEP 3: Scoring (FIXED)
        # ===============================
        if state["score"] is None:

            score_data = jd_scorer(
                state["summary"],
                skills=state["required_skills"]   
            )

            print("Observation:", score_data)

            state["score"] = score_data.get("score", 0)
            state["strengths"] = score_data.get("strengths", [])
            state["gaps"] = score_data.get("gaps", [])

            # role match
            role_keywords = ["backend", "api", "flask", "django"]
            text = state["summary"].lower()

            state["role_match"] = any(k in text for k in role_keywords)

            continue

        # ===============================
        # STEP 4: Save
        # ===============================
        if not state.get("saved"):
            state["name"] = state["candidate"]
            insert_candidate(state)
            print("Saved to DB")
            state["saved"] = True
            continue

        # ===============================
        # STEP 5: Verify (FIXED)
        # ===============================
        
        if not state.get("verified"):
            record = get_by_name(state["candidate"])
            print("Observation:", record)
            if isinstance(record, list) and record:
                row = record[0]
                db_score = row[1]
                if db_score > state["score"]:
                    state["score"] = db_score
                state["summary"] = row[2] + " " + row[3]
            state["verified"] = True
            continue
       

        # ===============================
        # FINAL ANSWER
        # ===============================
        decision = decide(
            state["score"],
            state["summary"],
            state["has_profile"],
            state["role_match"]
        )

        print("\n--- FINAL ANSWER ---")
        print(f"{state['candidate']} scored {state['score']}/100.")
        print(f"Strengths: {', '.join(set(state['strengths']))}")
        print(f"Gaps: {', '.join(set(state['gaps']))}")
        print(f"Profile: {state['profile_url']}")
        print(f"Decision: {decision}")

        state["done"] = True
        break

    # ===============================
    # HARD STOP
    # ===============================
    if not state["done"]:
        print("\n--- FINAL ANSWER (FORCED STOP) ---")
        print(f"{state['candidate']} scored {state.get('score', 'N/A')}/100.")

        decision = decide(
            state.get("score", 0),
            state.get("summary", ""),
            state.get("has_profile", True),
            state.get("role_match", True)
        )

        print("Decision:", decision)