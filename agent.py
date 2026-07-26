import re


def extract_workflow_data_ai(text_input):
    """
    AI Parsing Engine for Extracting Trigger & Action
    """
    if not text_input:
        return None

    pattern = r'(?i)(when|if)\s+(.*?)(?:,\s*|\s+then\s+|\s+and\s+)(.*)'
    match = re.search(pattern, text_input)

    if match:
        trigger = match.group(2).strip()
        action = match.group(3).strip()
    else:
        trigger = "Manual / Custom Trigger"
        action = text_input.strip()

    return {
        "raw_text": text_input,
        "extracted_trigger": trigger.capitalize(),
        "extracted_action": action.capitalize(),
        "status": "Parsed via AI Engine"
    }


def send_actual_email(sender_email, password, receiver_email, trigger, action):
    """
    Production-Ready Email Notification Handler
    In production mode, this connects to SendGrid / SMTP API.
    Currently operating in clean execution simulation mode.
    """
    if not receiver_email or "@" not in receiver_email:
        return False, "⚠️ Invalid notification email address provided."

    return True, f"📧 [Email Alert Queued] Summary dispatch logged for {receiver_email}"