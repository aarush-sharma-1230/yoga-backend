from langchain_core.prompts import PromptTemplate

DEVELOPER_PROMPT = "You are a calm and professional yoga instructor guiding a user through a yoga session"


def _get_transition_query_prompt(transition_from_idx: int, postures):
    postures_context = ", ".join([f"{posture['name']}" for posture in postures])

    if transition_from_idx == -1:
        first_posture = postures[0]["name"]
        template = f"""Provide a concise and helpful transition instruction for a yoga session.

Here are the postures in the sequence: {postures_context}

Please narrate the transition to guide the user to go into the "{first_posture}" posture. This is the first posture of the session.

Ensure your response is under 100 words
"""
    else:
        template = f"""Provide a concise and helpful transition instruction for a yoga session.

Here are the postures in the sequence: {postures_context}

The user is currently in the "{postures[transition_from_idx]['name']}" posture.

Please narrate the transition to guide the user from the "{postures[transition_from_idx]['name']}" posture to the "{postures[transition_from_idx + 1]['name']}" posture.

Ensure your response is under 100 words
"""

    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()


def _get_user_query_prompt(postures, current_posture: str, chat_history, user_query: str):
    postures_context = ", ".join([f"{posture['name']}" for posture in postures])
    chat_context = "\n".join([f"User: {msg['human']}\nAI: {msg['ai']}" for msg in chat_history])

    template = f"""Provide a concise and helpful response, keeping it engaging and relevant to the user's current yoga session.

The user is currently in the "{current_posture}" posture.

Here is the chat history so far:
{chat_context}

Here are the postures in the sequence: {postures_context}

Now, the user is asking:
User: {user_query}

Ensure your response is under 100 words
"""
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()


def _get_start_user_session_prompt(sequence_name: str):
    template = f"""Begin by welcoming the user to the session "{sequence_name}",
    setting a mindful tone, and guiding them to focus on their breath.
    
    Ensure your response is under 100 words
    """
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()


def _get_end_user_session_prompt(sequence_name: str):
    template = f"""Conclude the yoga session "{sequence_name}" by:
    - Acknowledging the user's effort and dedication
    - Guiding them through a final moment of gratitude and reflection
    - Encouraging them to take this sense of calm and mindfulness forward
    - Ending with "Namaste" or a similar closing
    
    Ensure your response is under 100 words
    """
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()
