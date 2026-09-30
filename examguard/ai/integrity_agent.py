

from database import get_db
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_session_data(candidate_id, session_id):
    connection = get_db()
    
    try:
        score = connection.execute("""
                                   SELECT integrity_score, risk_level, event_penalty, face_presence_ratio,computed_at
                                   FROM integrity_scores
                                   WHERE candidate_id = ?
                                   AND session_id = ?
                                   """, (
            candidate_id,
            session_id
        )).fetchone()
        if score is None:
            raise ValueError(
                f"No integrity score found for "
                f"candidate_id={candidate_id}, "
                f"session_id={session_id}"
            )
    
        events = connection.execute("""
                                    SELECT event_type, event_time, details from browser_events
                                    WHERE candidate_id = ?  and session_id = ?
                                    """, (candidate_id, session_id)).fetchall()
        
        face_events = connection.execute("""
                                    SELECT started_at, ended_at, duration_seconds
                                    FROM face_events
                                    WHERE candidate_id = ?  and session_id = ?
                                    """, (candidate_id, session_id)).fetchall() 
        
        return {
            "score": score,
            "browser_events": [dict(event) for event in events],
            "face_events": [dict(event) for event in face_events]
        }

    finally:
        connection.close()
        
def prepare_report_context(session_data):
    score = session_data["score"]
    browser_events = session_data["browser_events"]
    face_events = session_data["face_events"]

    report_context = {
        "integrity_score": score["integrity_score"],
        "risk_level": score["risk_level"],
        "event_penalty": score["event_penalty"],
        "face_presence_ratio": score["face_presence_ratio"],
        "computed_at": score["computed_at"],
        "browser_events": browser_events,
        "face_events": face_events
    }

    return report_context

# Langchain
# session data (database)-> langchain->llm->integrity report

# python -m pip install langchain langchain-openai

# Create the langchain prompt:


def create_report_prompt():

    prompt = ChatPromptTemplate.from_template("""
You are an examination integrity reporting assistant.

Your job is to analyze the provided examination
session data and generate an evidence-based report.

SESSION INFORMATION

Integrity Score:
{integrity_score}

Risk Level:
{risk_level}

Event Penalty:
{event_penalty}

Face Presence Ratio:
{face_presence_ratio}%

Report Computed At:
{computed_at}


BROWSER EVENTS

{browser_events}


FACE MONITORING EVENTS

{face_events}


REPORT REQUIREMENTS

1. Explain the integrity score.

2. Explain the risk level.

3. Summarize the face monitoring information.

4. Summarize the browser activity.

5. Mention important observed events.

6. Use only the information provided.

7. Do not invent events or values.

8. Do not change or recalculate the integrity score.

9. Do not claim that an event proves misconduct.

10. Treat the result as a review-support report.

Write the report in a clear and professional format.
""")

    return prompt


# ChatPromptTemplate : create a resuable prompt template for ai chat interaction

def test_prompt():
    context={
        "integrity_score": 85,
        "risk_level": "low",
        "event_penalty": 15,
        "face_presence_ratio": 98,
        "computed_at": "2024-06-01 12:00:00",
        "browser_events": [
            {"event_type": "tab_switch", "event_time": "2024-06-01 12:05:00", "details": None},
            {"event_type": "focus_loss", "event_time": "2024-06-01 12:10:00", "details": None}
        ],
        "face_events": [
            {"started_at": "2024-06-01 12:00:00", "ended_at": "2024-06-01 12:30:00", "duration_seconds": 1800}
        ]
    }
    prompt = create_report_prompt()
    messages=prompt.format_messages(**context)
    # format_message is a method which passes the actual values to placeholders
    for message in messages:
        print(message.content)
        
# Configure LLM

# database -> get_session_data -> prepare_report_context -> crete_prompt -> format_message -> llm -> genearte report

def create_llm():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    return llm

def test_llm():
    llm = create_llm()
    response = llm.invoke(
        "You are an examination integrity reporting assistant."
    )
    print("LLM Response:", response)
    
def create_integrity_report():
    prompt = create_report_prompt()
    llm = create_llm()
    chain = prompt | llm #runnable sequence
    # llm->prompt
    return chain
    
def test_integrity_report():
    context={
            "integrity_score": 85,
            "risk_level": "low",
            "event_penalty": 15,
            "face_presence_ratio": 98,
            "computed_at": "2024-06-01 12:00:00",
            "browser_events": [
                {"event_type": "tab_switch", "event_time": "2024-06-01 12:05:00", "details": None},
                {"event_type": "focus_loss", "event_time": "2024-06-01 12:10:00", "details": None}
            ],
            "face_events": [
                {"started_at": "2024-06-01 12:00:00", "ended_at": "2024-06-01 12:30:00", "duration_seconds": 1800}
            ]
        }
    chain = create_integrity_report()
    response = chain.invoke(context)

    print("\n==============================")
    print("EXAMGUARD INTEGRITY REPORT")
    print("==============================\n")

    print(response.content)
    
    

# chatopenai : creates connection between python application and openai chat model
# 

if __name__ == "__main__":
    # test_prompt()
    # test_llm()
     test_integrity_report()
