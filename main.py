#CORE CHATBOT LOGIC

from groq import Groq  #import groq AI
from config import GROQ_API_KEY # Import API key safely from config
from prompt_templates import SYSTEM_PROMPT  # Import the system prompt
from data_loader import lookup_sanctions, lookup_tariff

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


#ADD POLICY SAFETY LAYERS

def classify_intent(user_input):
    """
    Analyzes the user’s question for harmful intent 
    based on simple keyword detection.
    Categories:
        - 'dangerous'
        - 'sensitive'
        - 'safe'
    """

    user_input_lower = user_input.lower()

    # High-risk / dangerous intent (block completely)
    dangerous_keywords = [
        "evade sanctions",
        "bypass sanctions",
        "illegal arms",
        "how to launder money",
        "get around export controls",
        "help me hack",
        "violent overthrow",
        "bioweapon",
        "instructions to do something illegal"
    ]

    for keyword in dangerous_keywords:
        if keyword in user_input_lower:
            return "dangerous"

    # Sensitive but allowed with safe, educational responses
    sensitive_keywords = [
        "sanctions",
        "export controls",
        "foreign policy",
        "national security",
        "intelligence",
        "diplomacy"
    ]

    for keyword in sensitive_keywords:
        if keyword in user_input_lower:
            return "sensitive"

    # Otherwise safe
    return "safe"

def safety_filter(user_input):
    """
    Applies safety rules based on the detected intent.
    """

    intent = classify_intent(user_input)

    if intent == "dangerous":
        return {
            "blocked": True,
            "response": (
                "I’m here to provide safe, legal, and educational information. "
                "I cannot assist with instructions related to evading sanctions, "
                "illegal activity, or harming people or nations."
            )
        }

    elif intent == "sensitive":
        return {
            "blocked": False,
            "prepend": (
                "Note: This topic involves sensitive geopolitical and policy issues. "
                "The following is an educational, general explanation and not actionable advice.\n\n"
            )
        }

    # No safety action needed
    return {"blocked": False}



#FUNCTION FOR CHATBOT RESPONSES

def generate_response(user_input, system_prompt):
    # 'system' → instructions to the model (SYSTEM_PROMPT)
    # 'user'   → the user's question
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

# Call GROQ API model
# temperature → controls randomness (0 = deterministic, 1 = creative)
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )

        # Extract the text from the API response
        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        # Handle errors (network issues, API limits, etc.)
        return f"Error generating response: {e}"



# TESTING CHATBOT- MAIN FUNCTION

def main():
    print("Welcome to the Geopolitical Policy Chatbot!")
    print("Type 'exit' to quit.\n")

    # **Quick instructions for Step 5 lookups
    print("Step 5 Dataset Lookup Instructions:")
    print("1. To look up a sanction from the OFAC SDN list:")
    print("   Type: lookup sanction <entity_name>")
    print("   Example: lookup sanction Cuba\n")

    print("2. To look up a WTO MFN applied tariff:")
    print("   Type: lookup tariff <reporting_country> <partner_country> <year>")
    print("   Example: lookup tariff \"United States\" China 2022\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower().startswith("lookup sanction"):
            name = user_input.replace("lookup sanction", "").strip()
            print(lookup_sanctions(name))
            continue

        if user_input.lower().startswith("lookup tariff"):
            parts = user_input.split()
            reporting_country = parts[2]
            partner_country = parts[3] if len(parts) > 3 else None
            year = parts[4] if len(parts) > 4 else None
            print(lookup_tariff(reporting_country, partner_country, year))
            continue

        # Check safety before generating response
        safety = safety_filter(user_input)

        if safety["blocked"]:   #handles both true and false cases
            print(f"Bot: {safety['response']}\n")
            continue

        # Prepare input with optional disclaimer
        input_for_llm = user_input
        if "prepend" in safety:  # sensitive topic
             # wrap in tags so the model must repeat it first
            input_for_llm = (
                "<DISCLAIMER>\n"
                + safety["prepend"].strip()
                + "\n</DISCLAIMER>\n\n"
                + user_input
            )

        # Generate final model response
        answer = generate_response(input_for_llm, SYSTEM_PROMPT)
        print(f"Bot: {answer}\n")

#run main function after checking direct run from main
if __name__ == "__main__":
    main()

