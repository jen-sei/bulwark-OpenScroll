# AI-Agent Architecture

# Bulwark AI Agent Architecture

Bulwark is built as a **modular, intelligent system** that integrates multiple DeFi protocols, **AI-driven analytics**, and **user-friendly interfaces**. The AI agent architecture is organized into clearly defined, interconnected components, each responsible for distinct functionality. This design ensures a **robust, scalable, and efficient** operation.

---

## 1. Agent Runtime (FastAPI Backend)

The **core runtime environment** of the Bulwark agent is built on **Python’s FastAPI framework** and deployed via **Render.com**. It handles incoming requests, orchestrates interactions with DeFi protocols, manages internal state, and serves responses to the frontend application.

### **Responsibilities**
- Exposing **RESTful API endpoints** (`/api/generate-strategies`, `/api/ask`, etc.).
- Processing **incoming wallet and market data** requests.
- Managing **stateful interactions** with DeFi protocol services.
- Implementing **error handling, validation**, and **secure environment management**.

---

## 2. Providers (DeFi Protocol Integrations)

Providers act as the agent’s **"senses"**, offering **real-time** and **context-rich** information from **DeFi protocols on Scroll**.

### **a) AAVE V3 Provider**
- Fetches **market data**, including **real-time borrowing/lending APYs**.
- Retrieves **user-specific data** such as **health factor, liquidation thresholds**, and **available borrow limits**.

### **b) Ambient DEX (CrocSwap) Provider**
- Queries **pool data** (**prices, liquidity levels**).
- Simulates **token swaps** to determine **price impacts** and **liquidity requirements**.

### **c) Quill Finance Provider**
- Provides **collateral-based borrowing data**.
- Calculates **maximum borrowable USDQ amounts** based on **collateral types (ETH, SRC)**.
- Manages **stability pool data** and **liquidation risks**.

### **Implementation**
- Dedicated service files: `aave_service.py`, `ambient_service.py`, `quill_service.py`.
- **Real-time blockchain data fetching** and **caching mechanisms**.

---

## 3. AI Engine (Strategy Generator with LLM Integration)

The **AI-powered strategy generator** represents the **"brain"** of the Bulwark agent. Leveraging **OpenAI's GPT models**, it analyzes **portfolio balances, market conditions, and risk factors** to recommend **tailored investment strategies**.

### **Key Functionalities**
- Accepts **sanitized wallet data** and **aggregated market information** from providers.
- Uses **advanced prompt engineering** to clearly communicate goals to **GPT models**.
- Categorizes strategies into **five distinct risk tiers**:
  1. **Anchor Strategy** – Conservative, stablecoin-oriented, low-volatility yields.
  2. **Zenith Strategy** – Moderate leverage and balanced exposure across multiple protocols.
  3. **Wildcard Strategy** – Highly aggressive, utilizing leverage, arbitrage, and dynamic swaps for maximum potential returns.

### **AI Decision Logic**
- Incorporates **dynamic risk assessment models** (**e.g., AAVE health factors, Quill liquidation ratios**).
- **Minimizes transaction costs** (**gas fees**) and integrates **intelligent rebalancing logic**.
- Provides **explainable, transparent recommendations** with **clear risk-level classifications**.

---

## 4. Memory & Knowledge System (Contextual Awareness)

Bulwark maintains a **rich contextual awareness** by integrating a **comprehensive, textual knowledge base** (`bulwark_context.txt`), which is directly accessible by the AI-powered chatbot.

### **Components**
- **Context file** stored securely in the backend.
- Integrated with the **`/api/ask` endpoint**, ensuring **detailed, accurate responses** to user queries about the Bulwark system.
- **Continuous updating capability**, allowing for **additional knowledge incorporation** or **protocol updates** without code refactoring.
