# ============================================================
# DAY 1 - FIRST AI API CALL + SWEET CRUMBS BAKERY CHATBOT
# ============================================================

!pip install -q openai

from google.colab import userdata
from openai import OpenAI

print("=" * 55)
print("DAY 1 - MY FIRST AI API CALL")
print("=" * 55)

# STEP 1: Read API key safely from Colab Secrets
api_key = userdata.get("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check Colab Secrets."
    )

print("\nAPI key loaded successfully!")

# STEP 2: Connect to Groq
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

print("Groq client connected successfully!")

# STEP 3: Make our first simple API call
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "Explain what an AI agent is in simple English."
        }
    ]
)

print("\nMY FIRST AI RESPONSE:")
print(response.choices[0].message.content)

# STEP 4: Display token usage
print("\nTOKEN USAGE:")
print("Input tokens:", response.usage.prompt_tokens)
print("Output tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)


# ============================================================
# TODAY'S BUILD - SWEET CRUMBS HOME BAKERY
# ============================================================

SYSTEM = """
ROLE:
You are the friendly AI assistant for Sweet Crumbs Home Bakery.

FACTS:
1. We bake cakes after receiving orders.
2. Orders require 24 hours' notice.
3. All cakes have eggless versions.
4. Plum cake costs Rs 500.
5. Chocolate cake costs Rs 650.
6. Cupcakes cost Rs 80.

RULES:
1. Never promise a delivery time.
2. Do not invent prices or bakery policies.
3. If information is not available, say:
   "I'll check with the owner."
4. Keep answers under 50 words.
5. Reply in English.
"""

bakery_response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    messages=[
        {
            "role": "system",
            "content": SYSTEM
        },
        {
            "role": "user",
            "content": "Can I get an eggless cake today evening?"
        }
    ]
)

print("\n" + "=" * 55)
print("SWEET CRUMBS BAKERY CHATBOT")
print("=" * 55)

print("\nCUSTOMER QUESTION:")
print("Can I get an eggless cake today evening?")

print("\nAI CHATBOT ANSWER:")
print(bakery_response.choices[0].message.content)

print("\nTOKEN USAGE:")
print("Input tokens:", bakery_response.usage.prompt_tokens)
print("Output tokens:", bakery_response.usage.completion_tokens)
print("Total tokens:", bakery_response.usage.total_tokens)

print("\nDAY 1 PRACTICAL TASK COMPLETED!")
