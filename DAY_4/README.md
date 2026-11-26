# CYVORA – Day 4
## AI-Powered Software Bug Detection & Auto-Fixing Agent

### 1. Project Overview

CYVORA is an AI-powered software debugging assistant developed using Python and Large Language Models (LLMs).

Day 4 focuses on adding tools to the AI agent, structured output, function calling, error handling, and report storage.

The system helps identify Python syntax errors, analyze code, suggest corrections, validate suggested fixes, and save debugging reports.

### 2. Objectives

- Understand why AI agents need tools.
- Implement custom tools using LangChain's `@tool` decorator.
- Use function calling to perform debugging tasks.
- Generate structured AI responses using Pydantic.
- Validate corrected Python code.
- Handle errors during API and Google Sheets connections.
- Store debugging reports.

### 3. Technologies Used

- Python
- Groq API
- OpenAI GPT-OSS-120B
- LangChain
- LangChain-Groq
- Pydantic
- Google Colab
- Google Sheets (optional)
- CSV

### 4. Features Implemented

**1. Python Syntax Checker**

Uses Python's `ast.parse()` to identify syntax errors without executing submitted code.

**2. AI Code Analysis**

Uses the Groq language model to identify possible code issues and suggest corrections.

**3. Structured Output**

Uses Pydantic's `BaseModel` and `Field` to organize AI responses into a fixed format.

The bug report includes:
- Issue type
- Severity
- Explanation
- Evidence
- Suggested fix
- Manual review requirement

**4. Fix Validator**

Checks whether the suggested Python code has valid syntax.

**5. Custom Agent Tools**

CYVORA includes four tools:

- `check_python_syntax`
- `analyze_python_code`
- `validate_python_fix`
- `save_debugging_report`

**6. Debugging Report Storage**

Stores debugging reports with timestamps, project names, issue summaries, severity, and status.

Google Sheets integration is supported. If Google authentication fails, the system uses local CSV storage as a fallback.

**7. LangChain AI Agent**

Uses LangChain's `create_agent()` to connect the language model with the custom debugging tools.

### 5. Working Process

1. User provides Python code.
2. CYVORA receives the code.
3. The syntax checker identifies syntax errors.
4. The AI analyzes the problem.
5. The AI suggests corrected code.
6. The fix validator checks the syntax of the suggested code.
7. The debugging report can be saved when requested.

### 6. Sample Input

```python
def check_number(a):
    if a > 5
        print("Number is greater than 5")
    return a
```

### 7. Sample Output

```text
Syntax Error detected!

Line: 3
Problem: expected ':'

Suggested correction:

def check_number(a):
    if a > 5:
        print("Number is greater than 5")
    return a

FIX VALIDATION PASSED!
```

### 8. Report Storage

Debugging reports are stored in:

`CYVORA_Day4_Reports.csv`

If Google Sheets authentication is successful, reports can instead be saved in the Google spreadsheet:

`CYVORA_Day4_Debugging_Reports`

### 9. API Key Configuration

The Groq API key is stored securely in Google Colab Secrets.

Secret name:

`GROQ_API_KEY`

The API key is not included in the source code or GitHub repository.

### 10. How to Run

1. Open the Day 4 Google Colab notebook.
2. Add your Groq API key to Colab Secrets.
3. Run the installation and import section.
4. Execute the complete CYVORA code.
5. Enter Python code or debugging questions.
6. Review the AI-generated analysis and suggested correction.

### 11. Safety and Limitations

- Submitted Python code is never executed.
- Syntax validation does not guarantee logical correctness.
- AI-generated corrections require human review.
- Google Sheets requires successful Google authentication.
- CSV storage is available as a fallback.
- AI responses may occasionally contain incorrect suggestions.

### 12. Day 4 Learning Outcomes

Through Day 4, I learned how to:

- Create custom tools using LangChain.
- Understand AI function calling.
- Build an AI agent with multiple tools.
- Generate structured responses using Pydantic.
- Validate suggested Python fixes.
- Handle authentication and tool errors.
- Store debugging reports using CSV and Google Sheets integration.

### 13. Conclusion

Day 4 improved CYVORA by adding custom debugging tools, structured AI output, syntax validation, and report storage.

The project now uses a LangChain agent to assist with software debugging tasks and provides a foundation for building a more advanced autonomous software engineering platform.
