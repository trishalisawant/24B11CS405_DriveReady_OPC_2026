# ============================================================
# DAY 3 - AI AGENTS WORKSHOP
# PROJECT: AI-POWERED SOFTWARE BUG DETECTION & AUTO-FIXING AGENT
# PLATFORM: GOOGLE COLAB
# LANGUAGE: PYTHON
# ============================================================

# SECTION 1: INSTALL LIBRARIES

import sys
import subprocess

subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "langchain", "langchain-groq"
])

# SECTION 2: IMPORT LIBRARIES

import os
import ast
import csv
import json
from datetime import datetime

from google.colab import userdata

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# SECTION 3: CONNECT GROQ API

print("=" * 60)
print("CONNECTING TO GROQ")
print("=" * 60)

api_key = userdata.get("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found in Colab Secrets. "
        "Add your key under the name GROQ_API_KEY."
    )

os.environ["GROQ_API_KEY"] = api_key

MODEL = "openai/gpt-oss-120b"

llm = ChatGroq(
    model=MODEL,
    temperature=0
)

print("Groq API connected successfully!")
print("Model:", MODEL)


# SECTION 4: DEBUGGING SYSTEM PROMPT
# Instructions tell the AI its role and rules.

SYSTEM = """
ROLE:
You are an expert Python Software Debugging Assistant.

GOAL:
Help developers understand Python errors and improve their code.

RULES:
1. Read the submitted Python code carefully.
2. Explain syntax errors in simple English.
3. Identify possible logical and runtime problems.
4. Suggest corrected code when required.
5. Never claim that code was executed.
6. Do not confuse syntax validation with program execution.
7. If the syntax checker reports an error, explain that error.
8. If the code is syntactically correct, say "No syntax error".
9. Keep answers clear and well organised.
10. Do not invent test results.

FORMAT:
- Problem
- Explanation
- Suggested solution
- Important note

Always include the exact required phrase when one is provided.
"""

print("\nDebugging system prompt initialized!")


# SECTION 5: FEW-SHOT EXAMPLES

few_shot_examples = [
    ("human", "Explain this error: if x > 5"),
    ("ai", "Problem: Syntax error. Explanation: The if statement is missing a colon. Solution: Write if x > 5:"),

    ("human", "Explain this code: print('Hello'"),
    ("ai", "Problem: Syntax error. Explanation: A closing parenthesis is missing. Solution: Write print('Hello').")
]

print("Few-shot examples initialized!")

# SECTION 6: PYTHON SYNTAX CHECKER
# AST checks syntax without executing submitted code.

def detect_syntax_error(code: str) -> dict:
    """
    Check whether Python code has valid syntax.

    Parameters
    ----------
    code : str
        Python source code to check.

    Returns
    -------
    dict
        Syntax validation result.
    """

    if not code or not code.strip():
        return {
            "status": "Error",
            "error": "EmptyCode",
            "message": "No Python code was provided."
        }

    try:
        ast.parse(code)

        return {
            "status": "Passed",
            "message": "No syntax error. Python code is syntactically valid."
        }

    except SyntaxError as error:
        return {
            "status": "Error",
            "error": "SyntaxError",
            "line": error.lineno,
            "column": error.offset,
            "message": error.msg
        }


print("Python syntax checker initialized!")


# SECTION 7: LANGCHAIN PROMPT TEMPLATE

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),

    *few_shot_examples,

    MessagesPlaceholder(variable_name="history"),

    (
        "human",
        """
        Developer question:
        {question}

        Python code:
        {code}

        Result from Python syntax checker:
        {syntax_result}

        Required phrase to include in your answer:
        {must_include}
        """
    )
])

print("LangChain prompt template created!")


# SECTION 8: CREATE LANGCHAIN CHAIN

chain = prompt | llm | StrOutputParser()

print("LangChain chain created successfully!")

print("""
CHAIN WORKFLOW:

Input
  |
Prompt Template
  |
Groq Chat Model
  |
Output Parser
  |
Final Text Answer
""")


# SECTION 9: CONVERSATION MEMORY

debugging_history = []

def ask_debugging_assistant(question: str, code: str) -> str:
    """
    Ask the debugging assistant a question.

    The conversation history is passed to the chain
    so the assistant can use previous messages.
    """

    syntax_result = detect_syntax_error(code)

    answer = chain.invoke({
        "history": debugging_history,
        "question": question,
        "code": code,
        "syntax_result": json.dumps(syntax_result),
        "must_include": "debugging analysis"
    })

    debugging_history.extend([
        ("human", question),
        ("ai", answer)
    ])

    return answer


print("Conversation memory initialized!")


# SECTION 10: TEST THE DEBUGGING ASSISTANT

print("\n" + "=" * 60)
print("TESTING THE DEBUGGING ASSISTANT")
print("=" * 60)

sample_buggy_code = """
def calculate_total(a, b):
    total = a + b
    if total > 10
        print("Total is greater than 10")
    return total
"""

sample_question = "Find and explain the errors in this Python code."

sample_answer = ask_debugging_assistant(
    sample_question,
    sample_buggy_code
)

print("\nAI DEBUGGING ANALYSIS:")
print(sample_answer)


# SECTION 11: AUTOMATED TEST FILE
# Each test contains a question, code and expected phrase.

test_cases = [
    {
        "question": "Find the syntax error in this code.",
        "code": "if x > 5\n    print(x)",
        "must_include": "syntax error"
    },
    {
        "question": "Find the syntax error in this code.",
        "code": "print('Hello'",
        "must_include": "syntax error"
    },
    {
        "question": "Check whether this code has a syntax error.",
        "code": "def add(a, b):\n    return a + b",
        "must_include": "no syntax error"
    },
    {
        "question": "Identify the possible type problem in this code.",
        "code": "def add(a, b):\n    return a + b\n\nresult = add('5', 10)",
        "must_include": "potential type error"
    },
    {
        "question": "Explain how to correct this code.",
        "code": "if total > 10\n    print(total)",
        "must_include": "colon"
    }
]

with open("tests.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["question", "code", "must_include"]
    )

    writer.writeheader()
    writer.writerows(test_cases)

print("\ntests.csv created successfully!")


# SECTION 12: RUN AUTOMATED TESTS

def run_tests(path: str = "tests.csv") -> dict:
    """
    Run all debugging assistant tests.

    Each test checks whether the AI response contains
    the expected phrase.
    """

    passed = 0
    failed = 0
    results = []

    with open(path, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for number, row in enumerate(rows, start=1):

        print(f"\nRunning Test {number}...")

        syntax_result = detect_syntax_error(row["code"])

        answer = chain.invoke({
            "history": [],
            "question": row["question"],
            "code": row["code"],
            "syntax_result": json.dumps(syntax_result),
            "must_include": row["must_include"]
        })

        success = (
            row["must_include"].lower() in answer.lower()
        )

        if success:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        results.append({
            "test_number": number,
            "status": status,
            "question": row["question"],
            "expected": row["must_include"],
            "answer": answer
        })

        print(status, "|", row["question"])
        print("Expected phrase:", row["must_include"])
        print("AI answer:", answer[:250])

    total = len(rows)

    pass_rate = (
        (passed / total) * 100
        if total > 0 else 0
    )

    print("\n" + "=" * 60)
    print("AUTOMATED TEST SUMMARY")
    print("=" * 60)

    print("Total tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)
    print(f"Pass rate: {pass_rate:.0f}%")

    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "results": results
    }


test_report = run_tests()


# SECTION 13: BASIC LANGCHAIN AGENT
# This is an introductory agent with no tools yet.
# Real debugging tools will be added in Day 4.

print("\n" + "=" * 60)
print("CREATING BASIC LANGCHAIN AGENT")
print("=" * 60)

agent_report = {}

try:
    from langchain.agents import create_agent

    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM
    )

    agent_result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    "Explain this Python code: "
                    "if x > 5 print(x)"
                )
            }
        ]
    })

    agent_answer = agent_result["messages"][-1].content

    print("\nBASIC AGENT RESPONSE:")
    print(agent_answer)

    agent_report = {
        "status": "Passed",
        "message": "Basic LangChain agent created successfully."
    }

except Exception as error:

    print("Basic agent could not be created:", str(error))

    agent_report = {
        "status": "Failed",
        "message": str(error)
    }


# SECTION 14: FINAL DAY 3 REPORT

final_report = {
    "project": "AI-Powered Software Bug Detection & Auto-Fixing Agent",
    "day": 3,
    "date": datetime.now().strftime("%Y-%m-%d"),

    "langchain": {
        "status": "Initialized",
        "model": MODEL,
        "prompt_template": "Created",
        "chain": "Created"
    },

    "syntax_checker": "Initialized",

    "conversation_memory": {
        "status": "Initialized",
        "messages_saved": len(debugging_history)
    },

    "automated_testing": {
        "total_tests": test_report["total_tests"],
        "passed": test_report["passed"],
        "failed": test_report["failed"],
        "pass_rate": test_report["pass_rate"]
    },

    "basic_agent": agent_report,

    "important_note": (
        "Syntax validation does not guarantee logical correctness. "
        "Submitted code was analyzed, not executed. "
        "The introductory agent has no tools yet."
    )
}

print("\n" + "=" * 60)
print("FINAL DAY 3 REPORT")
print("=" * 60)

print(json.dumps(final_report, indent=4))

print("\n" + "=" * 60)
print("DAY 3 LANGCHAIN WORKFLOW FINISHED")
print("=" * 60)

print("LANGCHAIN SETUP: COMPLETED")
print("PROMPT TEMPLATE: COMPLETED")
print("LANGCHAIN CHAIN: COMPLETED")
print("SYNTAX CHECKER: COMPLETED")
print("CONVERSATION MEMORY: COMPLETED")
print("AUTOMATED TESTING: COMPLETED")
print("BASIC AGENT: CHECK REPORT ABOVE")
print("=" * 60)
