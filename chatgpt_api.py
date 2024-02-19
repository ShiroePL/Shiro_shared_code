# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
from openai import OpenAI

def send_to_openai(messages):
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature = 0.6
        )
        if completion.choices:
            answer = completion.choices[0].message.content
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens
        else:
            print("completion.choices is empty!")
    # Handle it accordingly
        
        
        
        return answer, prompt_tokens, completion_tokens, total_tokens

    except openai.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        return f"Error: {e.args[0]}", 0, 0, 0

    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        return "OpenAI API is currently overloaded", 0, 0, 0

    except openai.error.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        if 'timed out' in str(e):
            return "Request to OpenAI API timed out", 0, 0, 0
        else:
            return f"Error: {e.args[0]}", 0, 0, 0


async def send_to_openai_local(messages):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    try:
        completion = client.chat.completions.create(
            model="local-model",
            messages=messages,
            temperature=0.6,
            stream=True
        )

        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        print(f"An error occurred: {e}")
        yield f"Error: {e.args[0]}"



#   #completion_tokens = result[2] or _,_,completion_tokens,_ = result if i would like ot take only one


if __name__ == "__main__":
    # answer, prompt_tokens, completion_tokens, total_tokens = send_to_openai()
    # print("answer: " + answer)
    # print("prompt_tokens: " + str(prompt_tokens))
    # print("completion_tokens: " + str(completion_tokens))
    # print("total_tokens: " + str(total_tokens))
    pass
    
