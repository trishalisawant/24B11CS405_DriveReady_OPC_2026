# Day 3 – AI-Powered Software Bug Detection & Auto-Fixing Agent

## Project Overview

The **AI-Powered Software Bug Detection & Auto-Fixing Agent** is a Python-based AI project that helps developers identify and understand errors in Python code.

On Day 3, I implemented the basic LangChain structure and created a debugging assistant using the Groq AI model.

The system analyzes submitted code, checks for syntax errors, explains problems, and provides suggestions to fix them.

## Objectives

- Understand the difference between a chatbot and an AI agent.
- Learn the basic concepts of LangChain.
- Connect an AI model using Groq.
- Create prompts using `ChatPromptTemplate`.
- Use few-shot examples to improve AI responses.
- Build a debugging assistant using a LangChain chain.
- Maintain basic conversation history.
- Create and run automated test checks.

## Technologies Used

- **Programming Language:** Python
- **Development Platform:** Google Colab
- **AI Model:** `openai/gpt-oss-120b`
- **AI Framework:** LangChain
- **LLM Provider:** Groq
- **Libraries:** `ast`, `csv`, `json`, `datetime`, `langchain`, `langchain-groq`

## Features Implemented

### 1. Groq API Connection
Connected the Groq API and initialized the AI model.

### 2. Syntax Error Detection
Used Python's AST module to identify syntax errors in submitted Python code.

### 3. Few-Shot Prompting
Added examples to help the AI understand how to explain common coding errors.

### 4. LangChain Prompt Template
Created a structured prompt using `ChatPromptTemplate`.

### 5. Debugging Assistant
Built a LangChain chain that analyzes code and provides explanations and suggestions.

### 6. Conversation Memory
Stored conversation messages in basic debugging history.

### 7. Automated Testing
Created a `tests.csv` file containing five test cases and checked the AI responses against expected phrases.

### 8. Basic LangChain Agent
Created a basic LangChain agent using `create_agent`.

## Project Workflow

1. Receive Python code from the user.
2. Check the code for syntax errors.
3. Send the code and syntax-checking result to the AI model.
4. Analyze the code using the LangChain chain.
5. Generate an explanation and suggested correction.
6. Store conversation history.
7. Perform automated response checks.
8. Generate a final execution report.

## Installation

Install the required libraries:

```bash
pip install langchain langchain-groq
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

## Testing Results

The Day 3 implementation completed the following checks:

| Test | Result |
|---|---|
| Groq API connection | Passed |
| LangChain prompt template | Created |
| LangChain chain | Created |
| Syntax checker | Initialized |
| Conversation history | Initialized |
| Automated test cases | 5/5 passed |
| Basic LangChain agent | Passed |

**Automated test result: 5/5 (100%)**

Note: The five tests check expected phrases in AI responses. They do not prove that every suggested correction is logically correct.

## Current Limitations

- The syntax checker identifies syntax errors but does not guarantee logical correctness.
- The submitted Python code is analyzed, not executed.
- The introductory LangChain agent currently has no tools connected.
- The automated tests use basic response checks.

## Day 3 Conclusion

Successfully implemented the basic LangChain structure for the AI-Powered Software Bug Detection & Auto-Fixing Agent.

The project now includes AI-based code analysis, syntax checking, prompt templates, conversation history, automated response testing, and a basic LangChain agent.

This implementation provides a foundation for adding more advanced agent capabilities in the next stages.
