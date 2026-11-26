
# ============================================================
# DAY 2 - AI AGENTS WORKSHOP
# PROJECT: AI-POWERED SOFTWARE BUG DETECTION & AUTO-FIXING AGENT
# ============================================================

# 1. INSTALL AND IMPORT LIBRARIES

import sys
import subprocess

subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q", "groq"
])

import ast
import json
from functools import wraps
from datetime import datetime
from google.colab import userdata
from groq import Groq


# 2. GROQ API CONNECTION

api_key = userdata.get("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Add it in Google Colab Secrets."
    )

client = Groq(api_key=api_key)

# Updated supported model
MODEL = "openai/gpt-oss-120b"

print("Groq API connected successfully!")


# 3. SYSTEM PROMPT

system_prompt = """
You are an expert AI Software Debugging Engineer.

Your responsibilities:
1. Analyze Python source code.
2. Identify syntax errors and possible logical bugs.
3. Explain the root cause of each issue.
4. Suggest corrected code.
5. Never claim code is correct without checking it.
6. Return clear and structured debugging reports.
7. Do not execute submitted source code.
"""

print("\nSystem prompt initialized!")


# 4. MESSAGES AND ROLES

messages = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": "What are your responsibilities as a debugging AI?"
    }
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.2
)

print("\n========== AI ROLE ==========")
print(response.choices[0].message.content)


# 5. FEW-SHOT PROMPTING

few_shot_messages = [
    {
        "role": "system",
        "content": """
        You are a Python debugging assistant.

        Example 1:
        Buggy code: print("Hello"
        Error: Missing closing parenthesis.
        Correction: print("Hello")

        Example 2:
        Buggy code: if x > 5 print(x)
        Error: Missing colon after the condition.
        Correction: if x > 5:
                         print(x)

        Learn from these examples and analyze new code.
        """
    },
    {
        "role": "user",
        "content": "Find the problem in: for i in range(5) print(i)"
    }
]

few_shot_response = client.chat.completions.create(
    model=MODEL,
    messages=few_shot_messages,
    temperature=0.2
)

print("\n========== FEW-SHOT DEBUGGING ==========")
print(few_shot_response.choices[0].message.content)


# 6. PYTHON DICTIONARY AND JSON

bug_report = {
    "file": "sample.py",
    "bug_type": "Syntax Error",
    "line": 2,
    "description": "Missing colon after if statement",
    "status": "Detected"
}

print("\n========== BUG REPORT ==========")
print(json.dumps(bug_report, indent=4))


# 7. DECORATOR FOR DEBUGGING LOGS

def debugging_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
        print(f"Starting: {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Completed: {func.__name__}")
        return result

    return wrapper


# 8. SYNTAX ERROR DETECTION USING AST

@debugging_logger
def detect_syntax_error(code: str) -> dict:
    """Check Python source code for syntax errors."""

    try:
        ast.parse(code)

        return {
            "status": "Success",
            "error": None,
            "message": "No syntax errors detected."
        }

    except SyntaxError as error:

        return {
            "status": "Error",
            "error": "SyntaxError",
            "line": error.lineno,
            "column": error.offset,
            "message": error.msg
        }


# 9. AI-POWERED BUG ANALYSIS

@debugging_logger
def analyze_code_with_ai(code: str) -> str:
    """Ask AI to explain bugs in the submitted Python code."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
                    Analyze the following Python code.

                    Identify:
                    1. Syntax errors.
                    2. Possible logical errors.
                    3. Root causes.
                    4. Suggested corrections.

                    Do not execute the code.

                    CODE:
                    {code}
                    """
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI analysis failed: {error}"



import re

@debugging_logger
def automatic_code_fixer(code: str) -> str:
    """Generate and syntax-check corrected Python code."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert Python code fixer.

                    Return the complete corrected Python code
                    inside a Python code block.

                    Preserve the original functionality.
                    Do not execute the submitted code.
                    """
                },
                {
                    "role": "user",
                    "content": f"Fix this Python code:\n\n{code}"
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content or ""

        # Extract code from a Python Markdown block
        match = re.search(
            r"```(?:python)?\s*(.*?)```",
            answer,
            re.DOTALL | re.IGNORECASE
        )

        if match:
            cleaned = match.group(1).strip()
        else:
            cleaned = answer.strip()

        # Reject empty responses
        if not cleaned:
            raise ValueError("AI returned empty corrected code.")

        # Validate syntax
        ast.parse(cleaned)

        return cleaned

    except Exception as error:
        return f"Code fixing failed: {error}"

# 11. DEBUGGING MEMORY

debugging_memory = []

def remember_debugging_step(code, report, fixed_code=None):

    debugging_memory.append({
        "timestamp": datetime.now().isoformat(),
        "original_code": code,
        "bug_report": report,
        "fixed_code": fixed_code
    })

    print("\nDebugging step saved in memory!")


# 12. COMPLETE DEBUGGING PIPELINE

@debugging_logger
def run_debugging_agent(code: str) -> dict:
    """Detect, analyze, fix and validate Python code."""

    print("\n========== ORIGINAL CODE ==========")
    print(code)

    # Step A: Detect syntax errors
    syntax_result = detect_syntax_error(code)

    print("\n========== SYNTAX CHECK ==========")
    print(json.dumps(syntax_result, indent=4))

    # Step B: AI analysis
    print("\n========== AI BUG ANALYSIS ==========")
    ai_analysis = analyze_code_with_ai(code)
    print(ai_analysis)

    # Step C: Generate correction
    print("\n========== AUTOMATIC CODE FIX ==========")
    fixed_code = automatic_code_fixer(code)
    print(fixed_code)

    # Step D: Validate corrected code
    print("\n========== FIX VALIDATION ==========")

    if fixed_code.startswith("Code fixing failed:"):
        validation = {
            "status": "Failed",
            "message": fixed_code
        }

    else:
        try:
            ast.parse(fixed_code)

            validation = {
                "status": "Passed",
                "message": "Corrected code has valid Python syntax."
            }

        except SyntaxError as error:
            validation = {
                "status": "Failed",
                "message": error.msg,
                "line": error.lineno
            }

    print(json.dumps(validation, indent=4))

    # Step E: Save debugging memory
    remember_debugging_step(
        code,
        ai_analysis,
        fixed_code
    )

    return {
        "syntax_check": syntax_result,
        "ai_analysis": ai_analysis,
        "fixed_code": fixed_code,
        "validation": validation
    }


# 13. TEST WITH SAMPLE BUGGY CODE

sample_buggy_code = '''
def calculate_total(a, b):
    total = a + b
    if total > 10
        print("Total is greater than 10")
    return total
'''

print("\n" + "=" * 60)
print("AI SOFTWARE BUG DETECTION AGENT - DAY 2")
print("=" * 60)

result = run_debugging_agent(sample_buggy_code)


# 14. FINAL STRUCTURED JSON REPORT

final_report = {
    "project": "AI Software Bug Detection & Auto-Fixing Agent",
    "day": 2,
    "syntax_check": result["syntax_check"],
    "ai_analysis": result["ai_analysis"],
    "fixed_code": result["fixed_code"],
    "validation": result["validation"],
    "memory_entries": len(debugging_memory)
}

print("\n========== FINAL DEBUGGING REPORT ==========")
print(json.dumps(final_report, indent=4))


# 15. PROJECT COMPLETION

print("\n" + "=" * 60)
print("DAY 2 DEBUGGING PIPELINE FINISHED")
print("AI ANALYSIS: COMPLETED")
print("AUTOMATIC FIX GENERATION: ATTEMPTED")
print("SYNTAX VALIDATION: COMPLETED")
print("DEBUGGING MEMORY: UPDATED")
print("=" * 60)

print("\nIMPORTANT:")
print("Syntax validation does not guarantee logical correctness.")
print("Submitted code was analyzed, not executed.")
