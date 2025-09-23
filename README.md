# ChatBet Technical Assessment

This project is a **sports betting conversational agent**.  
It integrates with the provided sports & betting API and offers a **natural conversational experience** for querying matches, teams, tournaments, and odds.

---

## 🚀 Features
- **Conversational AI Agent** capable of understanding natural language queries about sports, odds, and bets.  
- **Context Management** using **LangGraph + LangChain**, allowing the agent to maintain memory across conversations.  
- **Secure Authentication** ensuring user tokens and personal details remain private from the AI.  
- **Modular Architecture** with clear separation of services, tools, and models for easy maintenance and scalability.  
- **Structured Settings Management** with Pydantic for clean handling of environment variables.  
- **User-Friendly Interface** powered by **Streamlit** for a simple and pleasant interaction.

---

## 🏗️ Architecture & Technical Decisions

### **1. LangGraph + LangChain**
- **Why**: Combining **LangGraph** with **LangChain** provides robust **conversational memory**, making it easier for the agent to keep context during multi-turn conversations.  
- **Benefit**: The agent can recall previous user messages, handle follow-ups naturally, and maintain a consistent conversation thread.

### **2. Pydantic for Models & Settings**
- **Usage**:  
  - **Output Models**: API responses are validated and typed with Pydantic, ensuring reliable and predictable data handling.  
  - **Tool Schemas**: Each tool has Pydantic-based schemas, enabling clear input/output definitions for the agent.  
  - **Environment Management**: `pydantic-settings` simplifies loading and validating environment variables.
- **Benefit**: Guarantees type safety and keeps configuration modular and easy to modify.

### **3. Modular Service Layer**
- **Service Folder**: Handles all **API calls** (authentication, fixtures, odds, bets) with minimal logic.  
- **Tools Folder**: Contains the logic that the AI agent uses to call services, making it easier for the agent to identify and execute available tools.  
- **Benefit**: Clear separation of concerns enhances maintainability and scalability.

### **4. Authentication & Privacy**
- **Goal**: The bot should never have direct access to **user tokens**, IDs, or private data.  
- **Implementation**: Authentication logic securely stores tokens in the backend, exposing only the necessary context to the AI.

### **5. Streamlit UI**
- **Why**: Provides a lightweight, interactive, and visually pleasant web interface for testing and showcasing the chatbot.
