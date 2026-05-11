from langchain_groq import ChatGroq
from config import GROQ_API_KEY
import re

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY
)

def score_candidate(summary, jd="Python backend developer"):

    prompt = f"""
    You are an expert recruiter.

    Job Description: {jd}

    Candidate Profile:
    {summary}

    Give output STRICTLY in this format:

    Score: <number between 0 and 100>
    Strengths: <comma separated points>
    Gaps: <comma separated points>
    """

    try:
        response = llm.invoke(prompt).content.strip()

        
        score_match = re.search(r"Score:\s*(\d+)", response)
        score = int(score_match.group(1)) if score_match else 50


        strengths_match = re.search(r"Strengths:\s*(.*)", response)
        strengths = (
            [s.strip() for s in strengths_match.group(1).split(",")]
            if strengths_match else ["Basic knowledge"]
        )

        # Extract gaps
        gaps_match = re.search(r"Gaps:\s*(.*)", response)
        gaps = (
            [g.strip() for g in gaps_match.group(1).split(",")]
            if gaps_match else ["Needs improvement"]
        )

        return {
            "score": score,
            "strengths": strengths,
            "gaps": gaps
        }

    except Exception:
        return {
            "score": 50,
            "strengths": ["Basic knowledge"],
            "gaps": ["Needs improvement"]
        }