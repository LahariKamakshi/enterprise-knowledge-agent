Enterprise Knowledge Agent

An AI-powered enterprise knowledge agent that continuously learns from organizational emails and stores important business knowledge in persistent memory using Hindsight. The system can recall previously learned information and provide grounded answers through a conversational interface.

🚀 Overview

Enterprise teams generate large amounts of information through emails, project updates, technical discussions, meetings, deployments, and operational decisions.

Important information can easily become difficult to find later.

The Enterprise Knowledge Agent solves this by automatically:

Reading Gmail messages
Identifying enterprise-relevant emails
Extracting useful facts from relevant emails
Storing those facts in Hindsight memory
Recalling relevant memories when a user asks a question
Generating an answer based only on the retrieved enterprise knowledge

The system is designed as a foundation for a larger organizational memory system that can later integrate sources such as Jira, Microsoft Teams, GitHub, SharePoint, and other enterprise applications.

🎯 Problem Statement

Enterprise information is distributed across multiple communication and collaboration platforms.

For example:

Project updates may be buried inside emails
Deployment decisions may be discussed weeks before implementation
Team responsibilities may change over time
Technical issues may be mentioned across multiple conversations
Important decisions can become difficult to retrieve

Traditional search can find messages, but it does not necessarily maintain a persistent understanding of the organization's knowledge.

The goal of this project is to create an AI agent that can learn, remember, and recall enterprise knowledge over time.

💡 Solution

The Enterprise Knowledge Agent creates a continuous memory pipeline:

Gmail
   ↓
Email Ingestion
   ↓
Relevance Detection
   ↓
LLM Fact Extraction
   ↓
Hindsight Memory
   ↓
Semantic Recall
   ↓
LLM
   ↓
Grounded Answer

Instead of manually entering information into the system, new relevant Gmail messages can automatically become part of the agent's organizational memory.

🧠 Why Hindsight?

Hindsight provides the persistent memory layer of the system.

The agent uses Hindsight to:

Store enterprise facts
Preserve information across conversations
Recall relevant historical knowledge
Perform semantic memory retrieval
Build a persistent organizational memory

This allows the agent to move beyond a simple chatbot architecture.

The system is designed around the idea that an enterprise agent should not only answer questions, but also remember information learned from previous organizational interactions.

🏗️ System Architecture
                   ┌──────────────────┐
                   │      Gmail       │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Email Ingestion  │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Relevance Filter │
                   │      (LLM)       │
                   └────────┬─────────┘
                            │
                    Relevant Emails
                            │
                            ▼
                   ┌──────────────────┐
                   │  Fact Extraction │
                   │      (LLM)       │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │    Hindsight     │
                   │ Persistent Memory│
                   └────────┬─────────┘
                            │
                     User Question
                            │
                            ▼
                   ┌──────────────────┐
                   │ Hindsight Recall │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │   Groq LLM       │
                   │ Grounded Answer  │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │  Streamlit UI    │
                   └──────────────────┘
✨ Key Features
1. Automatic Gmail Ingestion

The system connects to Gmail using the Gmail API and retrieves recent messages.

Relevant emails can automatically become part of the enterprise memory.

2. AI-Based Relevance Detection

Not every email contains useful organizational knowledge.

The system uses an LLM to classify emails as:

RELEVANT

or

IRRELEVANT

Examples of relevant information include:

Project updates
Technical issues
Deployment information
Team responsibilities
Deadlines
Architecture decisions
Database changes
Cloud infrastructure updates
Business decisions
Tasks and requirements

Examples of irrelevant information include:

Promotions
Newsletters
Shopping emails
Entertainment
Generic advertisements
3. Enterprise Fact Extraction

Relevant emails are processed by an LLM to extract structured enterprise knowledge.

For example, an email might contain:

Project Orion production deployment is scheduled
for October 3 at 10 PM IST.

David Miller will handle database deployment.
Priya Rao will monitor Azure SQL.
Lisa Johnson will perform post-deployment validation.

The system converts this information into concise enterprise memories.

4. Persistent Memory

Extracted facts are stored inside Hindsight.

Example:

Project Orion production deployment is scheduled
for October 3, 2026 at 10 PM IST.

The information remains available for future queries.

5. Semantic Recall

When a user asks a question, the system searches Hindsight for relevant memories.

Example:

User:
Who is responsible for the Project Orion database deployment?

The system retrieves the relevant organizational memory before generating the answer.

6. Grounded Answers

The final response is generated using the retrieved enterprise memories.

The system follows strict grounding rules:

Use only retrieved enterprise knowledge
Do not invent facts
Preserve numbers and dates
Do not create unsupported relationships
Do not combine unrelated information
Clearly state when the requested information is unavailable

This helps reduce hallucinated enterprise information.

7. Duplicate Prevention

The system maintains a local record of processed Gmail message IDs.

processed_emails.json

If an email has already been processed, the system skips it.

This prevents repeatedly storing the same email information in Hindsight.

📧 Gmail Integration

The project uses the Gmail API with OAuth authentication.

The first time the application connects to Gmail, the user authorizes access.

A local OAuth token is then stored so subsequent runs do not require repeated authentication.

The Gmail scope used by the project is:

https://www.googleapis.com/auth/gmail.readonly

The application only requires read access to Gmail.

🔐 Security

Sensitive credentials are kept outside the Git repository.

The following files should never be committed:

.env
client_secret.json
token.json
processed_emails.json

The .gitignore file excludes these files.

API keys are loaded through environment variables.

Example .env:

HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key

Never publish API keys or OAuth credentials in a public repository.

🛠️ Tech Stack
Programming Language
Python
AI / LLM
Groq
OpenAI-compatible LLM API
Memory
Hindsight
Email Integration
Gmail API
Google OAuth 2.0
User Interface
Streamlit
Development
VS Code
Git
GitHub
📁 Project Structure
memory-agent/
│
├── app.py
├── ingest_gmail.py
├── chat_agent.py
├── data.py
│
├── development/
│   ├── agent.py
│   ├── ask_agent.py
│   ├── final_agent.py
│   ├── email_classifier.py
│   ├── json_to_hindsight.py
│   ├── llm_extract.py
│   ├── llm_extract_json.py
│   ├── main.py
│   ├── memory.py
│   └── recall.py
│
├── test/
│   ├── gmail_test.py
│   └── llm_test.py
│
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/LahariKamakshi/enterprise-knowledge-agent.git

Navigate to the project:

cd enterprise-knowledge-agent

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
🔑 Environment Configuration

Create a .env file in the project root:

HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key

Replace the placeholder values with your own credentials.

📩 Gmail Setup
1. Create a Google Cloud project

Create a project in Google Cloud Console.

2. Enable Gmail API

Enable:

Gmail API
3. Configure OAuth Consent Screen

Configure the OAuth consent screen for the application.

4. Create OAuth Credentials

Create an OAuth client for a desktop application.

5. Download the credentials

Download the OAuth JSON file and rename it:

client_secret.json

Place it in the project root.

6. Authorize Gmail

Run the application.

A browser window will open for Gmail authorization.

After successful authentication:

token.json

will be created automatically.

🧠 Hindsight Setup

Create a Hindsight account and obtain an API key.

Configure the API key in .env:

HINDSIGHT_API_KEY=your_hindsight_api_key

The project uses the Hindsight API to create persistent enterprise memory and retrieve relevant memories.

The main memory bank used by the project is:

enterprise-knowledge
▶️ Running the Application

Activate the virtual environment:

venv\Scripts\activate

Start Streamlit:

streamlit run app.py

The application will open in the browser.

🔄 Automatic Learning Workflow

When the user asks a question, the application can first synchronize new Gmail information.

The workflow is:

User asks a question
        ↓
Check Gmail for new emails
        ↓
Skip previously processed emails
        ↓
Classify new emails
        ↓
Ignore irrelevant emails
        ↓
Extract facts from relevant emails
        ↓
Store facts in Hindsight
        ↓
Recall relevant enterprise memories
        ↓
Generate grounded answer

This allows the agent to continuously learn from new organizational information.

🧪 Example Scenario

Suppose an organization sends an email:

Subject:
Project Orion Production Deployment Update

The email contains:

Production deployment is scheduled for
October 3, 2026 at 10 PM IST.

David Miller will handle database deployment.
Priya Rao will monitor Azure SQL.
Lisa Johnson will perform post-deployment validation.

The maintenance window is 30 minutes.
A rollback plan is available.

The agent processes the email and stores the relevant information in Hindsight.

Later, a user can ask:

Who is responsible for the Project Orion database deployment?

The system recalls the relevant memory and can answer:

David Miller is responsible for the Project Orion
database deployment.
🧩 Example Enterprise Questions

The agent can be used for questions such as:

Who is managing Project Orion?
Who is responsible for the database deployment?
When is the production deployment scheduled?
Who is monitoring Azure SQL?
What technical issue was reported?
What was the latest project update?
Who is responsible for post-deployment validation?
What deployment window was communicated?
🧪 Testing

Basic components can be tested independently.

Run Gmail testing:

python test/gmail_test.py

Run LLM testing:

python test/llm_test.py

The individual development scripts can also be used to test memory ingestion, recall, extraction, and agent behavior.

🗃️ Memory Lifecycle

The project separates the memory workflow into multiple stages:

Source Data
    ↓
Ingestion
    ↓
Filtering
    ↓
Extraction
    ↓
Memory Storage
    ↓
Memory Retrieval
    ↓
Answer Generation

This separation makes it possible to add additional enterprise data sources without redesigning the complete system.

🔌 Future Integrations

The current implementation focuses on Gmail, but the architecture can be extended to additional enterprise sources.

Potential integrations include:

Gmail
   ↓
Microsoft Teams
   ↓
Jira
   ↓
GitHub
   ↓
SharePoint
   ↓
OneDrive

Each source can feed information into the same enterprise memory layer.

🚀 Future Improvements

Possible future improvements include:

Microsoft Teams integration
Jira ticket ingestion
GitHub activity ingestion
SharePoint document ingestion
Meeting transcript ingestion
Automatic conflict detection
Latest-information prioritization
Source-aware memories
Memory confidence scoring
Role-based enterprise access
Scheduled background ingestion
Enterprise dashboards
Multi-user organizational memory
Audit trails for retrieved information
🌐 Scalability

The architecture is designed so that additional data sources can be added without changing the core memory and answering system.

For example:

Gmail ────────┐
              │
Jira ─────────┤
              │
Teams ────────┤
              ├──→ Hindsight ──→ Agent
              │
GitHub ───────┤
              │
SharePoint ───┘

This makes Hindsight the central persistent memory layer for the enterprise agent.

🏆 Project Highlights

The project demonstrates:

AI-powered enterprise knowledge extraction
Persistent agent memory
Semantic memory retrieval
Gmail API integration
OAuth authentication
LLM-based relevance classification
LLM-based fact extraction
Automated ingestion
Duplicate prevention
Grounded answer generation
Streamlit application development
Modular Python architecture
Secure environment-variable configuration
📌 Key Idea

The core idea of the Enterprise Knowledge Agent is simple:

Instead of asking an AI agent to remember everything manually, allow it to continuously learn from organizational information and build persistent enterprise memory.

The result is an AI agent that can transform scattered organizational communication into searchable, persistent knowledge.
