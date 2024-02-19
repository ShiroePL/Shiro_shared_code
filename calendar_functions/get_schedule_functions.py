import pymysql
from datetime import datetime
from .chatgpt_calendar_prompts import CalendarAssistant


def extract_dates_from_answer(answer):
    start_date_str = answer.split(",")[0].split(":")[1].strip()
    end_date_str = answer.split(",")[1].split(":")[1].strip().rstrip(".")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    print(f"Inside extract_dates_from_answer: {type(start_date)}, {type(end_date)}")
    return start_date, end_date



def retrieve_plans_for_days(query: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
    query = f"{query}. today is : {current_time}"
    calendar_assistant = CalendarAssistant(model="gpt-3.5-turbo")
    answer, prompt_tokens, completion_tokens, total_tokens = calendar_assistant.chatgpt_calendar_schedule(query)
    
    print(f"answer: {answer}")  # answer is string
    
    # Extract dates from the answer
    start_date, end_date = extract_dates_from_answer(answer)
    
    print(f"start_date: {start_date}")
    print(f"end_date: {end_date}")
    
    print(type(start_date))
    print(type(end_date))
    
    # Uncomment this line after you are sure that start_date and end_date are of correct type
    # db_events = retrieve_events_from_user_table("example_username", start_date, end_date)
    
    return answer, start_date, end_date
