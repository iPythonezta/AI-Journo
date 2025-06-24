# AI Journalist

AI Journalist is an intelligent agent system that autonomously discovers, verifies, summarizes, and posts news updates on X.com (formerly Twitter), focusing on geopolitics, wars, conflicts, and other high-impact global events. It leverages multiple specialized agents and Selenium-based automation to interact with X.com, monitor breaking news, and engage with the online community.

---

## Features

- **Automated News Discovery:** Finds news from trusted sources (BBC, Reuters, CNN, Al Jazeera, Dawn, etc.).
- **Verification & Summarization:** Uses LLM-powered agents to summarize news in a concise, neutral, and factual manner.
- **Automated Posting:** Posts updates (including images) to X.com using a Selenium-driven bot.
- **Community Engagement:** Monitors and interacts with posts from trusted X.com accounts to detect breaking news and trending topics.
- **Image Handling:** Downloads, manages, and attaches relevant images to posts.
- **Memory Management:** Keeps track of processed news and actions to avoid duplication.

---

## Project Structure

```
AI Journalist/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── main_prompt.txt
├── writer_prompt.txt
├── x_agent_prompt.txt
├── research_agent_prompt.txt
├── README.md
├── cookies/           # Stores login cookies for X.com sessions
└── images/            # Stores images for posting
```

---

## Agents

- **MainAgent:** Orchestrates the workflow, manages memory, and coordinates sub-agents.
- **ResearchAgent:** Discovers and verifies news stories from credible sources.
- **WriterAgent:** Summarizes news for X.com posts, ensuring clarity and brevity.
- **XAgent:** Handles all X.com interactions (login, posting, searching, following, etc.) via the `Twitterbot` class.

---

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   - Create a `.env` file with your Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

4. **Prepare Images (Optional):**
   - Place any images you want to use for posts in the `images/` directory.

---

## Usage

Run the main script:

```sh
python main.py
```

You will be prompted for:
- Your X.com username/email and password (used for Selenium login).
- A prompt describing the news task or event to cover.

The system will:
1. Use the ResearchAgent to gather and verify news.
2. Summarize the news using the WriterAgent.
3. Post the update on X.com via the XAgent.

---

## Customization

- **Prompts:** Modify the `.txt` prompt files to adjust agent behavior and instructions.
- **Agent Logic:** Extend or modify `main.py` to add new tools, sources, or behaviors.
- **Image Handling:** Add images to the `images/` directory for use in posts.

---

## Security & Privacy

- User credentials are used only for browser automation and are not stored.
- Cookies are saved in the `cookies/` directory for session reuse.
- Do **not** share your `.env` or `cookies/` files publicly.

---

## Requirements

- Python 3.11 (Might be compatible with other versions but I haven't tested it)
- Google Chrome browser (for Selenium)
- See `requirements.txt` for Python dependencies.

---

## License

This project is for educational and research purposes only.

---

**Author:** [Your Name or Team]  
**Contact:** [Your Email or GitHub]