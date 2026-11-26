# Day 2 – AI-Powered Software Bug Detection & Auto-Fixing Agent

## Project Overview

The **AI-Powered Software Bug Detection & Auto-Fixing Agent** is a Python-based AI project that helps developers identify, understand, and fix errors in Python code.

On Day 2, I improved the basic debugging system by adding AI-based code analysis, automatic fix suggestions, debugging memory, structured responses, and error handling.

The system uses the Groq AI model to analyze Python code and suggest possible corrections.

## Objectives

- Understand system prompts and few-shot prompting.
- Generate structured AI responses using JSON.
- Learn about dictionaries and JSON handling.
- Create reusable Python functions with type hints.
- Implement decorators for logging.
- Handle errors using `try-except`.
- Build debugging memory.
- Develop an AI-based code analysis and fixing system.

## Technologies Used

- **Programming Language:** Python
- **Development Platform:** Google Colab
- **AI Model:** `openai/gpt-oss-120b`
- **LLM Provider:** Groq
- **Libraries:** `groq`, `json`, `re`, `ast`, `functools`

## Features Implemented

### 1. Groq API Integration
Connected the Groq API and initialized the AI model.

### 2. System Prompt
Created instructions that guide the AI model to behave as a Python debugging assistant.

### 3. Few-Shot Prompting
Provided example inputs and outputs to help the AI understand how to analyze coding errors.

### 4. Structured JSON Responses
Used JSON to organize bug reports and AI-generated debugging information.

### 5. Syntax Error Detection
Used Python's AST module to identify syntax errors in submitted code.

### 6. AI-Based Code Analysis
Used the AI model to explain coding problems and suggest possible solutions.

### 7. Automatic Code Fixing
Implemented a function that generates corrected Python code based on the identified errors.

### 8. Debugging Memory
Used a Python dictionary to store debugging information and previous debugging steps.

### 9. Logging Decorator
Implemented a decorator to record function execution and debugging activities.

### 10. Error Handling
Used `try-except` blocks to handle errors and improve the reliability of the program.

### 11. Fix Validation
Checked whether the generated code is non-empty and whether it passes Python syntax validation.

## Project Workflow

1. Receive Python code as input.
2. Check the code for syntax errors.
3. Analyze the code using the Groq AI model.
4. Generate a structured bug report.
5. Suggest a corrected version of the code.
6. Validate that the generated code is non-empty.
7. Check the corrected code using AST syntax validation.
8. Store debugging information in memory.
9. Display the debugging results.

## Installation

Install the required libraries:

```bash
pip install groq langchain langchain-groq pydantic
```

## API Key Configuration

A Groq API key is required.

Set the `GROQ_API_KEY` environment variable before running the program.

**Windows PowerShell:**

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

**Linux / macOS:**

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Never upload your actual API key to GitHub.

## How to Run

Run the Python file using:

```bash
python task.py
```

If running in Google Colab, configure the API key using Colab Secrets.

## Testing Results

The Day 2 implementation was tested using sample Python code containing a syntax error.

The system successfully:

- Identified the missing colon.
- Generated an explanation of the error.
- Suggested corrected Python code.
- Validated that the generated code was non-empty.
- Passed the syntax validation.
- Updated debugging memory.

## Current Limitations

- Syntax validation does not guarantee logical correctness.
- Generated code is not executed.
- AI-generated fixes may still require manual review.
- The debugging memory is basic and does not provide permanent storage.

## Day 2 Conclusion

Successfully improved the AI-Powered Software Bug Detection & Auto-Fixing Agent by adding structured AI responses, few-shot prompting, syntax validation, automatic fix suggestions, debugging memory, logging, and error handling.

These features provide a stronger foundation for developing more advanced AI agent capabilities in the next stages.
