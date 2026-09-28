# Enterprise Knowledge Agent

> An AI-powered enterprise knowledge agent that continuously learns from organizational emails and uses persistent memory to answer questions with context.

The **Enterprise Knowledge Agent** is an AI agent designed to solve a common enterprise problem: important information is scattered across emails, project updates, technical discussions, decisions, tasks, and operational communications.

Instead of treating every question as a new conversation, the agent continuously converts relevant Gmail messages into structured enterprise knowledge and stores that knowledge in **Hindsight**, a persistent memory system.

Users can then ask natural-language questions about projects, people, responsibilities, decisions, technical issues, deployments, and deadlines.

---

## Project Overview

In a typical organization, important information is distributed across multiple communication channels.

For example:

- A project manager may be mentioned in one email.
- A deployment date may be discussed in another.
- A technical issue may be reported several days later.
- A team member's responsibility may be defined in a meeting update.
- A resolution may appear in a completely different email.

Traditional chatbots often fail to connect these pieces of information because they do not maintain long-term organizational memory.

The Enterprise Knowledge Agent addresses this problem by creating a continuously updated memory layer.

### Core idea

```text
Gmail
  ↓
Email ingestion
  ↓
Relevance detection
  ↓
LLM-based fact extraction
  ↓
Hindsight persistent memory
  ↓
Memory retrieval
  ↓
Groq LLM
  ↓
Natural-language answer
