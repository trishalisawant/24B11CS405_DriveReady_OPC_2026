
# ============================================================
# CYVORA - DAY 4
# AI-POWERED SOFTWARE BUG DETECTION & AUTO-FIXING AGENT
#
# Features:
# 1. Groq LLM connection
# 2. Google Sheets integration (optional fallback)
# 3. Python syntax checking
# 4. AI bug analysis
# 5. Structured output using Pydantic
# 6. Python fix validation
# 7. Debugging report saving
# 8. LangChain agent with tools
#
# SAFETY:
# - User code is never executed.
# - Syntax validation does not prove logical correctness.
# - API keys are never printed or saved.
# ============================================================


# ============================================================
# 1. INSTALL LIBRARIES
# ============================================================

import sys
import subprocess

subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "groq",
    "langchain",
    "langchain-groq",
    "langchain-core",
    "pydantic",
    "gspread",
    "google-auth"
])

print("Libraries installed successfully!")


# ============================================================
# 2. IMPORT LIBRARIES
# ============================================================

import os
import ast
import json
import csv

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent

print("Libraries imported successfully!")


# ============================================================
# 3. CONNECT GROQ API
# ============================================================

from google.colab import userdata

GROQ_API_KEY = userdata.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in Colab Secrets. "
        "Add your key under the Secrets tab."
    )

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    max_retries=3,
    api_key=GROQ_API_KEY
)

print("Groq API connected successfully!")
print("Model: openai/gpt-oss-120b")


# ============================================================
# 4. CONNECT GOOGLE SHEETS SAFELY
# ============================================================

print("\nConnecting Google Sheets...")

gc = None
ws = None
SHEETS_CONNECTED = False

try:
    from google.colab import auth
    import gspread
    from google.auth import default

    # Authenticate Google account
    auth.authenticate_user()

    # Get Google credentials
    credentials, project = default()

    # Authorize Google Sheets
    gc = gspread.authorize(credentials)

    # Open existing spreadsheet or create a new one
    spreadsheet_name = "CYVORA_Day4_Debugging_Reports"

    try:
        sh = gc.open(spreadsheet_name)
        print("Existing Google Sheet opened!")

    except gspread.SpreadsheetNotFound:
        sh = gc.create(spreadsheet_name)
        print("New Google Sheet created!")

    ws = sh.sheet1

    # Add column headings
    headers = [
        "Timestamp",
        "Project",
        "Issue Summary",
        "Severity",
        "Status"
    ]

    if not ws.get_all_values():
        ws.append_row(headers)

    SHEETS_CONNECTED = True

    print("Google Sheets connected successfully!")
    print("Sheet URL:", sh.url)

except Exception as e:
    print("\nGoogle Sheets authentication was unsuccessful.")
    print("Reason:", str(e))
    print("CYVORA will use local CSV storage instead.")
    SHEETS_CONNECTED = False


# ============================================================
# 5. STRUCTURED BUG REPORT USING PYDANTIC
# ============================================================

class BugReport(BaseModel):

    issue_type: Literal[
        "Syntax Error",
        "Logic Error",
        "Security Concern",
        "Code Quality",
        "Unknown"
    ] = Field(description="Category of the detected issue")

    severity: Literal[
        "Low",
        "Medium",
        "High",
        "Critical"
    ] = Field(description="Estimated severity")

    explanation: str = Field(
        description="Simple explanation of the problem"
    )

    evidence: str = Field(
        description="Relevant code evidence"
    )

    suggested_fix: str = Field(
        description="Suggested correction"
    )

    requires_manual_review: bool = Field(
        description="Whether a human should review the suggestion"
    )


print("\nPydantic BugReport model created!")


# ============================================================
# 6. CREATE STRUCTURED OUTPUT MODEL
# ============================================================

bug_extractor = llm.with_structured_output(BugReport)

print("Structured output model initialized!")


# ============================================================
# 7. TOOL 1 - PYTHON SYNTAX CHECKER
# ============================================================

@tool
def check_python_syntax(code: str) -> str:
    """
    Check Python code for syntax errors using ast.parse.
    This tool never executes the submitted code.
    """

    if not code.strip():
        return "Error: Empty Python code received."

    try:
        ast.parse(code)

        return (
            "Syntax validation passed. "
            "No Python syntax errors were detected."
        )

    except SyntaxError as e:

        return (
            f"Syntax Error detected!\n"
            f"Line: {e.lineno}\n"
            f"Column: {e.offset}\n"
            f"Problem: {e.msg}"
        )

    except Exception as e:

        return f"Unexpected validation error: {str(e)}"


# ============================================================
# 8. TOOL 2 - AI CODE ANALYSIS
# ============================================================

@tool
def analyze_python_code(code: str) -> str:
    """
    Analyze Python code using the AI model.
    Returns a structured bug report.
    """

    if not code.strip():
        return "Error: Cannot analyze empty code."

    prompt = f"""
You are CYVORA, an AI software debugging assistant.

Analyze the following Python code.

Identify:
1. The type of issue.
2. Its severity.
3. A simple explanation.
4. Evidence from the submitted code.
5. A suggested correction.
6. Whether manual review is required.

Do not claim that code was executed.
Do not invent test results.

PYTHON CODE:

{code}
"""

    try:

        result = bug_extractor.invoke(prompt)

        if isinstance(result, BaseModel):
            return result.model_dump_json(indent=2)

        return json.dumps(result, indent=2)

    except Exception as e:

        return (
            "Structured AI analysis failed. "
            f"Reason: {str(e)}"
        )


# ============================================================
# 9. TOOL 3 - PYTHON FIX VALIDATOR
# ============================================================

@tool
def validate_python_fix(fixed_code: str) -> str:
    """
    Validate whether the suggested Python fix has valid syntax.
    Does not execute the code or prove logical correctness.
    """

    if not fixed_code.strip():
        return "Validation failed: AI returned empty code."

    try:

        ast.parse(fixed_code)

        return (
            "FIX VALIDATION PASSED!\n"
            "The suggested code has valid Python syntax.\n"
            "Note: Logical correctness has not been verified."
        )

    except SyntaxError as e:

        return (
            "FIX VALIDATION FAILED!\n"
            f"Line: {e.lineno}\n"
            f"Problem: {e.msg}"
        )

    except Exception as e:

        return f"Validation error: {str(e)}"


# ============================================================
# 10. PYDANTIC MODEL FOR DEBUGGING RECORD
# ============================================================

class DebuggingRecord(BaseModel):

    project: str = Field(min_length=1)

    issue_summary: str = Field(min_length=1)

    severity: Literal[
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    status: Literal[
        "Detected",
        "Suggested",
        "Syntax Validated",
        "Needs Manual Review"
    ]


# ============================================================
# 11. TOOL 4 - SAVE DEBUGGING REPORT
# ============================================================

@tool
def save_debugging_report(
    project: str,
    issue_summary: str,
    severity: str,
    status: str
) -> str:
    """
    Save a debugging summary to Google Sheets if connected.
    Otherwise, save it to a local CSV file.
    Call this tool only when the user explicitly requests saving.
    Do not save source code or API keys.
    """

    try:

        record = DebuggingRecord(
            project=project,
            issue_summary=issue_summary,
            severity=severity,
            status=status
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        row = [
            timestamp,
            record.project,
            record.issue_summary,
            record.severity,
            record.status
        ]

        # Save to Google Sheets
        if SHEETS_CONNECTED and ws is not None:

            ws.append_row(row)

            return "Debugging report saved successfully to Google Sheets."

        # Fallback: save to CSV
        csv_file = "CYVORA_Day4_Reports.csv"

        file_exists = os.path.exists(csv_file)

        with open(
            csv_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Timestamp",
                    "Project",
                    "Issue Summary",
                    "Severity",
                    "Status"
                ])

            writer.writerow(row)

        return (
            f"Debugging report saved locally to {csv_file}."
        )

    except Exception as e:

        return f"Could not save report: {str(e)}"


# ============================================================
# 12. REGISTER ALL AGENT TOOLS
# ============================================================

TOOLS = [
    check_python_syntax,
    analyze_python_code,
    validate_python_fix,
    save_debugging_report
]

print("\nCYVORA Tools Registered:")

for tool_item in TOOLS:
    print("-", tool_item.name)


# ============================================================
# 13. CYVORA SYSTEM PROMPT
# ============================================================

SYSTEM = """
You are CYVORA, an AI-powered software debugging assistant.

Your responsibilities:

1. Understand the user's Python code.
2. Identify possible software problems.
3. Use the syntax checker when appropriate.
4. Use AI code analysis to create a structured bug report.
5. Suggest corrected code when requested.
6. Validate suggested code using the syntax validator.
7. Save reports only when the user explicitly asks.

IMPORTANT RULES:

- Never execute user-submitted code.
- Never claim that code was executed.
- Never claim that a syntax check proves logical correctness.
- Explain technical problems in simple English.
- Do not invent test results.
- Do not save reports unless the user asks.
- Do not reveal API keys or credentials.
- Recommend manual review for uncertain or serious issues.
"""


# ============================================================
# 14. CREATE LANGCHAIN AI AGENT
# ============================================================

agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM
)

print("\nCYVORA AI Agent created successfully!")


# ============================================================
# 15. CONVERSATION MEMORY
# ============================================================

history = []


# ============================================================
# 16. CHAT FUNCTION
# ============================================================

def chat(question):

    global history

    if not question.strip():
        print("Please enter a question.")
        return

    try:

        messages = history + [
            {
                "role": "user",
                "content": question
            }
        ]

        response = agent.invoke({
            "messages": messages
        })

        answer = response["messages"][-1].content

        history = response["messages"]

        print("\nCYVORA RESPONSE:")
        print("=" * 60)
        print(answer)
        print("=" * 60)

        return answer

    except Exception as e:

        print("\nAgent error:", str(e))
        return None


# ============================================================
# 17. TEST CYVORA WITH SAMPLE BUGGY CODE
# ============================================================

buggy_code = """
def check_number(a):
    if a > 5
        print("Number is greater than 5")
    return a
"""

print("\n" + "=" * 60)
print("CYVORA DAY 4 TESTING")
print("=" * 60)


# Test syntax checker
print("\n1. TESTING SYNTAX CHECKER")

syntax_result = check_python_syntax.invoke({
    "code": buggy_code
})

print(syntax_result)


# Test AI structured analysis
print("\n2. TESTING AI BUG ANALYSIS")

analysis_result = analyze_python_code.invoke({
    "code": buggy_code
})

print(analysis_result)


# Test fix validation
print("\n3. TESTING FIX VALIDATOR")

sample_fixed_code = """
def check_number(a):
    if a > 5:
        print("Number is greater than 5")
    return a
"""

validation_result = validate_python_fix.invoke({
    "fixed_code": sample_fixed_code
})

print(validation_result)


# ============================================================
# 18. TEST THE AI AGENT - CORRECTED
# ============================================================

print("\n4. TESTING LANGCHAIN AGENT")

agent_question = f"""
Analyze the following Python code.

Find the syntax error.
Explain the problem.
Suggest corrected code.
Use the available tools.

Do not execute the code.

Python code:

{buggy_code}
"""

chat(agent_question)

# ============================================================
# 19. TEST REPORT SAVING
# ============================================================

print("\n5. TESTING REPORT STORAGE")

save_result = save_debugging_report.invoke({
    "project": "CYVORA",
    "issue_summary": "Missing colon in Python if statement",
    "severity": "Medium",
    "status": "Syntax Validated"
})

print(save_result)


# ============================================================
# 20. FINAL PROJECT STATUS
# ============================================================

print("\n" + "=" * 60)
print("CYVORA DAY 4 - FINAL REPORT")
print("=" * 60)

print("Groq API: Connected")
print("AI Model: openai/gpt-oss-120b")
print("Syntax Checker: Initialized")
print("AI Bug Analysis: Initialized")
print("Structured Output: Initialized")
print("Fix Validator: Initialized")
print("Debugging Report Tool: Initialized")
print("LangChain Agent: Initialized")

if SHEETS_CONNECTED:
    print("Google Sheets: Connected")
else:
    print("Google Sheets: Not connected")
    print("Report Storage: Local CSV fallback")

print("Code Execution: Disabled")
print("Safety: User code is not executed")

print("=" * 60)


# ============================================================
# 21. INTERACTIVE CYVORA CHAT
# ============================================================

print("\nCYVORA is ready!")
print("Type 'exit' to stop the chat.")
print("Example: Explain this Python error.")

while True:

    user_question = input("\nYou: ").strip()

    if user_question.lower() in ["exit", "quit", "stop"]:
        print("CYVORA session ended.")
        break

    if user_question:
        chat(user_question)
