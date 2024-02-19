from datetime import datetime
import re
from .chatgpt_calendar_prompts import CalendarAssistant
from . import calendar_api_test as cal
from .. import connect_to_phpmyadmin

def add_event_from_shiro(query:str):
    """Adds event to calendar from shiro gui 
    returns:  answer, prompt_tokens, completion_tokens, total_tokens, |summary, description, dtstart, dtend| in formatted_query_to_calendar"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
    #print(current_time)
    query = f"{query}. today is : {current_time}"

    #print(query)
        #send query to chatgpt and get response in correct format
    calendar_assistant = CalendarAssistant(model="gpt-3.5-turbo")
    # print(assistant.chatgpt_calendar_planer("Add a meeting to my calendar next Monday at 10 AM"))
    answer, prompt_tokens, completion_tokens, total_tokens = calendar_assistant.chatgpt_calendar_planer(query)

        # add event to calendar using api
    summary, description, dtstart, dtend = cal.add_event_to_calendar(answer)

    formatted_query_to_calendar = f"\nsummary: {summary} \ndescription: {description} \ndate: {dtstart} \nend_date: {dtend}"

    return answer, prompt_tokens, completion_tokens, total_tokens, formatted_query_to_calendar


def get_schedule_for_day(discord_username, answer_from_chatgpt):
    # Function to extract dates from the given text
    def extract_dates(text):
        matches = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        return [datetime.strptime(match, '%Y-%m-%d') for match in matches]
    
    # Extracting the dates from the answer
    dates = extract_dates(answer_from_chatgpt)
    start_date = dates[0]
    end_date = dates[1]

    # Fetch events from the MySQL database
    db_events = connect_to_phpmyadmin.retrieve_events_from_user_table(discord_username, start_date, end_date)
    
    formatted_result = ""
    # Loop through database events
    for event in db_events:
        formatted_result += f"Summary: {event['summary']}\n"
        formatted_result += f"Starts at: {event['date']}\n"
        formatted_result += f"Ends at: {event['end_date']}\n"
        formatted_result += f"Description: {event['description']}\n\n"

    # Here, you would add your existing code for fetching events from the CalDAV server.
    # Add those events to formatted_result as well.
    return formatted_result

def retrieve_plans_for_days(query:str):
    """Adds event to calendar from shiro's gui.
    This function first calls chatgpt to extract info from answer then calls calendar api to get schedule for specified days 
    returns:  answer, prompt_tokens, completion_tokens, total_tokens"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
    #print(current_time)
    query = f"{query}. today is : {current_time}"

    #print(query)
        #send query to chatgpt and get response in correct format
    calendar_assistant = CalendarAssistant(model="gpt-3.5-turbo")
    answer, prompt_tokens, completion_tokens, total_tokens = calendar_assistant.chatgpt_calendar_schedule(query)
        # add event to calendar using api
    

    

    return answer, prompt_tokens, completion_tokens, total_tokens