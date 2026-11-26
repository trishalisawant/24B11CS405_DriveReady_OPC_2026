# Day 1 – AI-Powered Software Bug Detection & Auto-Fixing Agent

## Project Overview

The **AI-Powered Software Bug Detection & Auto-Fixing Agent** is a Python-based AI project designed to help developers identify and understand errors in Python code.

On Day 1, I connected the Groq AI model and implemented the basic code analysis system to detect syntax errors and identify possible coding issues.

The project uses AI to explain errors and suggest possible corrections.

## Objectives

- Understand the basics of Large Language Models (LLMs).
- Connect an AI model using the Groq API.
- Learn how AI can help in software debugging.
- Detect syntax errors in Python code.
- Identify possible code issues.
- Generate AI-based explanations and suggestions.

## Technologies Used

- **Programming Language:** Python
- **Development Platform:** Google Colab
- **AI Model:** `openai/gpt-oss-120b`
- **LLM Provider:** Groq
- **Libraries:** `ast`, `groq`, `langchain`, `langchain-groq`

## Features Implemented

### 1. Groq API Connection
Connected the Groq API and initialized the AI model.

### 2. Syntax Error Detection
Used Python's AST module to check Python code for syntax errors.

### 3. Code Analysis
Analyzed Python code to identify possible coding issues, such as unused variables.

### 4. AI-Based Error Explanation
Used the AI model to explain detected errors in simple language.

### 5. Automatic Fix Suggestions
Generated suggested corrections for the identified code problems.

## Project Workflow

1. Provide Python code as input.
2. Check the code using the Python AST module.
3. Identify syntax errors.
4. Analyze possible coding issues.
5. Send the code to the AI model.
6. Receive an explanation and suggested correction.

## Installation

Install the required libraries:

```bash
pip install groq langchain langchain-groq
```

## API Key Configuration

A Groq API key is required to connect to the AI model.

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

## Day 1 Conclusion

Successfully established the basic foundation of the AI-Powered Software Bug Detection & Auto-Fixing Agent.

The implementation includes Groq API integration, syntax error detection, basic code analysis, AI-based error explanations, and suggested code corrections.

This forms the foundation for the advanced debugging and agent capabilities developed in the following days.
