import re

def format_code_blocks(text):
    """
    Replaces code wrapped in triple backticks with <code> tags.
    """
    # Regular expression to match code wrapped in triple backticks
    formatted_text = re.sub(r'```(.*?)```', r'<code>\1</code>', text, flags=re.DOTALL)
    return formatted_text
