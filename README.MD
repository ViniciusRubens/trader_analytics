# Trader Analytics: AI-Powered Stock Market Analytics

### About the project
This project delivers a robust, real-time trading analytics designed to support financial decision-making. Spanning from secure data ingestion to multi-agent AI analysis, the system utilizes **Streamlit** for the frontend, **yfinance** for market data, and **Phidata** integrated with **Groq (Llama 3)** to orchestrate a team of AI agents that summarize breaking news and analyst recommendations.

### Problem
Retail investors and traders often struggle to rapidly synthesize the vast amounts of quantitative (price action, moving averages, volume) and qualitative (latest news, analyst ratings) data available in the market. Doing this manually across multiple platforms is inefficient and prone to cognitive overload. Furthermore, directly querying financial APIs often leads to rate-limit bans, disrupting the flow of information during critical trading hours. 

### Solution
I developed a modular, Object-Oriented application that:
1.  Ingests historical market data dynamically based on user-provided ticker symbols.
2.  Protects backend infrastructure using a custom-patched session with caching (`requests-cache`) and rate limiting (`requests-ratelimiter`) to prevent API blocks.
3.  Orchestrates a Multi-Agent AI Team (Web Search Agent + Financial Agent) to fetch, synthesize, and present qualitative market context.
4.  Generates interactive, responsive data visualizations (Candlesticks, SMAs, EMAs, Volume) using **Plotly**.
5.  Provides an intuitive, styled UI with built-in educational and legal disclaimers.

### Tech stack
* **Language:** Python
* **Frontend/UI:** Streamlit
* **AI & Orchestration:** Phidata (Agents), Groq API (llama-3.3-70b-versatile, llama-3.1-8b-instant)
* **Data Ingestion:** yfinance, DuckDuckGo (Web Search)
* **Data Manipulation:** Pandas
* **Visualization:** Plotly (Express & Graph Objects)

---

### Data Source & Pipeline

**Source:** The application aggregates data from two primary streams:
* **Quantitative Data:** Historical price, volume, and moving averages fetched via the Yahoo Finance API.
* **Qualitative Data:** Web search results and analyst recommendations fetched via DuckDuckGo and Yahoo Finance tools.

**Pipeline:**
1.  **Ingestion:** The user submits a ticker via the Streamlit UI.
2.  **Validation & Shielding:** `MarketDataService` intercepts the request, passing it through a local SQLite cache and a rate limiter (max 2 requests/5s) before hitting the API.
3.  **Processing:** Data is formatted into Pandas DataFrames; technical indicators (20-day SMA, 20-day EMA) are calculated on the fly.
4.  **Multi-Agent Analysis:** The `AITradingTeam` triggers two agents simultaneously—one searching the web for news, the other scraping financial recommendations. A primary Llama-3 model synthesizes their findings into clean Markdown.
5.  **Rendering:** Data is pushed to `StockVisualizer` to render interactive Plotly charts alongside the AI summary in the frontend.

---

## Getting Started

Follow these instructions to set up a local copy of the project.

### Prerequisites

In this project I used `conda` for environment management.
* Ensure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

### Installation


1.  **Clone the repository** (or download the files to a local folder).
    ```bash
    git clone git@github.com:ViniciusRubens/trader_analytics.git
    cd your-repository-name
    ```

2.  **Create a new conda environment** (this example uses `project_env` as the name):
    ```bash
    conda create --name project_env python=3.12
    ```

3.  **Activate the new environment:**
    ```bash
    conda activate project_env
    ```

4.  **Install pip** into the environment:
    ```bash
    conda install pip
    ```

5.  **Install the required dependencies** from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage


With your `project_env` environment still active, run the application using the following command to start Streamlit application:

```bash
./run.sh
```

You can now view the UI in your browser at `http://localhost:8501/` 

You will see something like that in browser:

![](/assets/images/trader_homepage.png)

---

## How it Works (Step-by-Step)

1. **Configuration**: The application is initialized via `run.sh`, which verifies the presence of the `.env` file (containing the crucial `GROQ_API_KEY`) and launches the Streamlit server.

2. **Layout & UI**: The `AppLayout` class renders the custom CSS, top navigation bar (with GitHub/LinkedIn links), and handles the user input for the stock ticker.

3. **Safe Data Fetching**: The `MarketDataService` utilizes a globally patched `yf.Ticker` initialization. This ensures that all data requests—whether from the main app or the AI tools—are routed through `CachedLimiterSession`, preventing Yahoo Finance rate limits.

4. **AI Execution**: The `AITradingTeam` receives the ticker and prompts a multi-agent system. The *Web Search Agent* finds context, while the *Financial Agent* pulls analyst data. The orchestrating model cleans the internal tool logs and returns a cohesive summary.

5. **Visualization**: The `StockVisualizer` plots the retrieved historical data into multiple interactive components: a standard line chart, a Candlestick chart, Moving Averages (SMA & EMA), and a Volume bar chart.

---

## Cleanup

To deactivate and remove the conda environment (optional).

1.  **Deactivate the environment:**
    ```bash
    conda deactivate
    ```

2.  **Remove the environment (optional):**
    ```bash
    conda remove --name project_env --all
    ```

---

## License

Distributed under the MIT License. See `LICENSE` file for more information.