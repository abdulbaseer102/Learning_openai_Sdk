# AI Multi-Agent Routing System

## Overview

This project is designed to demonstrate a multi-agent AI system using **Chainlit**, **OpenAI SDK**, and **CrewAI** for intelligent message routing, streaming, and decision-making.

## Project Structure

### 1. `agent.py`

Defines the core **AI agent** structure, including:

- AI model initialization
- Agent roles and behaviors
- Input and output processing

### 2. `guardrails.py`

- Implements **Guardrails** to enforce rules and prevent unwanted input/output.
- Example: Restricts AI from solving math-related queries.

### 3. `handoffs.py`

- Implements **handoff logic** to switch between agents based on user input.
- Ensures seamless conversation flow between different AI agents.

### 4. `history.py`

- Manages conversation **history**.
- Stores previous interactions to maintain context.

### 5. `routing.py`

- Implements a **multi-language routing system**.
- Uses a triage agent to **route messages** to appropriate language-based agents (English, French, Spanish, etc.).

### 6. `streaming.py`

- Handles **real-time AI response streaming** using Chainlit.
- Ensures smooth and continuous message delivery.

### 7. `tool.py`

- Provides additional **utility functions** to support AI agents.

## Setup Instructions

### 1. Install Dependencies

Ensure you have Python installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file and add your **Gemini API Key**:

```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Run the Application

Start the Chainlit application:

```bash
chainlit run routing.py
```

## Features

- 🌍 **Multi-language AI Routing** (English, French, Spanish)
- ⚡ **Real-time Streaming Responses**
- 🛡️ **Guardrails for Controlled Outputs**
- 🔀 **Seamless Agent Handoffs**
- 📜 **Persistent Conversation History**

---

🚀 **Developed for AI-driven intelligent conversations!**

