from config import BOT_PRE_PROMPT, OPEN_AI_MODEL, OPEN_AI_TEMPERATURE, OPEN_AI_MAX_TOKENS

def openai_chat_completion(message_for_openai, message, openai):
    response = openai.ChatCompletion.create(
            model=OPEN_AI_MODEL,
            max_tokens=OPEN_AI_MAX_TOKENS,
            n=1,
            stop=None,
            temperature=OPEN_AI_TEMPERATURE,
            user=str(message.chat.id),
            messages=[
                {"role": "system", "content": BOT_PRE_PROMPT},
                {"role": "user", "content": message_for_openai},
            ]
        )
    return response['choices'][0]['message']['content']