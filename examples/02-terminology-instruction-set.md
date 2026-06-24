# Example 2 — "write the instruction set… make it an api" — terminology drift

## The original prompt
What a newer programmer might actually type:

> i need to write the instruction set for a customer service chatbot. it should answer questions about our return policy and never make up info it doesnt know. also can you make it into an api so our website can call it

---

## Without the skill
A coding agent takes the prompt at face value and runs with it:

# Customer Service Chatbot: Return Policy Assistant

Here's everything you need: a system prompt (instruction set) for the chatbot and a simple API so your website can call it.

---

## Part 1: Chatbot System Prompt (Instruction Set)

This is what you paste into the "system" field when calling the AI model.

```
You are a customer service assistant for [Company Name]. Your job is to help customers with questions about our return policy.

**What you do:**
- Answer questions about our return policy clearly and helpfully
- Be friendly, concise, and professional
- If a customer seems frustrated, acknowledge their concern before answering

**What you never do:**
- Never make up information you don't have. If you don't know something, say so directly and tell the customer how to get a real answer (e.g., "I don't have that information — please contact our support team at [email] or call [phone number].")
- Never guess at policy details. If you're unsure whether something is covered, say you're not sure and direct them to a human agent.
- Never promise refunds, exceptions, or outcomes you can't guarantee.

**Our Return Policy (use only this information to answer questions):**
[PASTE YOUR ACTUAL RETURN POLICY HERE — for example:]
- Items can be returned within 30 days of purchase
- Items must be unused and in original packaging
- Sale items are final sale and cannot be returned
- Refunds are issued to the original payment method within 5-7 business days
- To start a return, customers visit [returns URL] or email [returns email]

**If a customer asks something not covered above:**
Say: "I don't have that information available right now. For the most accurate answer, please reach out to our support team at [contact info] and they'll be happy to help."


> _…baseline truncated — the full no‑skill response ran 169 lines (it just started building)._

---

## With Vibecode Check

## Clarifying questions (with recommended defaults)

Before rewriting, here are the load-bearing gaps I need to close. You can reply **"use the defaults"** and I'll proceed, or answer only the ones that matter to you:

**1. Which AI service are you building on top of?**
Options: OpenAI (GPT-4o), Anthropic Claude, Google Gemini, or other.
*Default: OpenAI GPT-4o — most widely used and documented for this exact use case.*

**2. Which language/framework for the API endpoint?**
Options: Python + FastAPI, Node.js + Express, or a no-code tool (n8n, Zapier, etc.).
*Default: Python + FastAPI — clean, minimal, well-documented, and easy to deploy. FastAPI also auto-generates interactive docs at `/docs` so your team can test the endpoint immediately.*

**3. Do you have the actual return policy written down?**
The system prompt needs the real policy text — without it, the bot can only say "I don't have that information," which isn't useful. You can paste it now, write it as bullet points, or use a placeholder for now.
*Default: I'll write the system prompt with a clearly marked `[PASTE YOUR RETURN POLICY HERE]` section you fill in before deploying.*

**4. Where will the API run?**
Local dev server for now, or a cloud host (Render, Railway, AWS Lambda, Vercel)?
*Default: local dev server, with a note pointing to Render/Railway for when you're ready to go live.*

---

*Proceeding on all defaults.*

---

## 1. The cleaned-up prompt

```
You are a coding agent. Build a Python + FastAPI HTTP API endpoint that wraps an OpenAI GPT-4o chatbot configured to answer customer questions about our return policy.

## What to build

### System prompt (write this first)
Write a system prompt — the standing instructions the model receives at the start of every conversation — with these rules:
- The bot's only job is to answer questions about the return policy.
- It must stay strictly within the return policy text provided below. If a question isn't covered by the policy, it must say something like: "I don't have information on that — please contact our support team at [EMAIL]." It must never guess or make up an answer.
- Tone: friendly and concise.

Use this return policy text:
[PASTE YOUR RETURN POLICY HERE — e.g. "Items can be returned within 30 days with receipt. Sale items are final sale. Refunds are issued to the original payment method within 5–7 business days."]

### API endpoint
Build a single POST endpoint at `/chat` using FastAPI.

**Request body (JSON):**
```json
{
  "message": "What is your return window?"
}
```

**Response body (JSON):**
```json
{
  "reply": "You can return items within 30 days of purchase with a receipt."
}
```

The endpoint should:
1. Accept the user's message from the request body.
2. Call the OpenAI API (model: `gpt-4o`) with the system prompt above and the user's message.
3. Return the model's reply as JSON.
4. Use the `OPENAI_API_KEY` environment variable for the API key — never hardcode it.

## Stack
- Python 3.11+
- FastAPI
- `openai` Python SDK (v1+)
- `python-dotenv` to load the API key from a `.env` file in local dev

## Project structure
Create:
- `main.py` — the FastAPI app and `/chat` endpoint
- `system_prompt.py` — the system prompt string as a constant (so it's easy to update separately)
- `.env.example` — showing `OPENAI_API_KEY=your-key-here` (do NOT create a real `.env` file)
- `requirements.txt`

## Out of scope
- Do not add conversation history / multi-turn memory for now (stateless only — each request is independent).
- Do not add a database, user authentication, or a frontend UI.
- Do not deploy to a cloud host — local dev only for now.

## Verification
After writing the code:
1. Show the exact commands to install dependencies and run the server locally.
2. Show a `curl` command that sends a test question to the `/chat` endpoint.
3. Show the expected JSON response so I can confirm it's working.
4. Confirm the server URL and that the interactive API docs are available at `http://localhost:8000/docs`.
```

---

## 2. What I changed & corrected — and the convention behind it

**Corrections (non-standard terms):**

- **"instruction set" → "system prompt":** In AI/LLM development, the *system prompt* is the standing instructions given to the model at the start of every conversation — it shapes the model's behavior for all subsequent messages. "Instruction set" is a non-standard term in this context (it more commonly refers to CPU opcodes, e.g., x86 instruction set architecture) and would confuse a coding agent. Every LLM provider, tutorial, and SDK uses "system prompt" — learning this term now will pay off everywhere.

- **"make it into an API" → "build a POST endpoint using FastAPI":** "API" describes a category of interface, not a specific thing to build. A coding agent would have to guess: a REST API? A webhook? A serverless function? A WebSocket? Naming FastAPI and a concrete `/chat` endpoint removes that fork. (If you specifically need a different framework or protocol, that's easy to swap in.)

**Changes (sharpening):**

- **Added a return policy placeholder:** The system prompt can't work without the actual policy text. I added a clearly marked `[PASTE YOUR RETURN POLICY HERE]` block so the agent knows to structure the code around it, and so you know exactly where to fill it in.

- **Operationalized "never make up info":** "Don't hallucinate" isn't a reliable instruction on its own — it's too abstract. The rewritten prompt tells the model *exactly what to say when it doesn't know* ("I don't have information on that — please contact our support team"). That's the concrete behavior a system prompt can actually enforce.

- **Named the file structure:** Without named files, a coding agent invents its own layout. Splitting the system prompt into `system_prompt.py` makes it easy to update the return policy later without touching the API logic.

- **Added an explicit out-of-scope clause:** Conversation history, auth, and a frontend are natural things a coding agent might add unprompted. Naming them as out-of-scope prevents that.

- **Added a verification step:** The original prompt had no way to confirm the build worked. The `curl` command + expected output closes the loop so you — and the agent — can confirm success without guessing.

- **Added API key security note:** Hardcoding an API key is a common beginner mistake. Flagging `OPENAI_API_KEY` as an environment variable and noting `.env.example` (not a real `.env`) teaches the correct pattern.

---

## 3. Assumptions & possible misunderstandings — are we still in sync?

- **I took "our website can call it" to mean a simple REST API (HTTP POST request returning JSON)** — the most common pattern for this. If your website uses a different protocol (WebSocket for streaming, GraphQL, etc.), correct me and I'll adjust.

- **I assumed OpenAI GPT-4o as the AI provider.** If you're using Anthropic Claude or another provider, the SDK and API call in `main.py` will differ — the system prompt logic and endpoint structure stay the same, but the model call changes. Say the word and I'll rewrite for your provider.

- **I assumed stateless (no conversation memory).** Each call to `/chat` is independent — the bot has no memory of previous messages from the same user. This is simpler to build and is often right for an FAQ-style return policy bot. If you want multi-turn conversation (the user can ask follow-up questions that reference earlier ones), that requires passing conversation history and is a meaningful additional feature — flag it and I'll add it.

- **I assumed local development first.** The code will run on your machine at `http://localhost:8000`. When you're ready to put it on the internet so your website can reach it in production, services like Render or Railway can host a FastAPI app in about 10 minutes — let me know when you get there.

- **The `[PASTE YOUR RETURN POLICY HERE]` placeholder must be filled in before the bot is useful.** A bot built on a placeholder will answer every question with "I don't have information on that." That's not a bug — it's the correct behavior for an empty policy — but it won't be useful until the real text is in.

---

## 4. Prompt tips for next time

**Tip 1 — "System prompt" is the term that unlocks everything.**
Every AI provider (OpenAI, Anthropic, Google), every tutorial, and every SDK uses the term *system prompt* for the standing instructions you give a chatbot. Now that you know the word, you'll find it everywhere — and coding agents will understand exactly what you mean. Compare: "write an instruction set" leaves an agent guessing; "write a system prompt that..." lands precisely.

**Tip 2 — End with a verification step.**
Notice I added a `curl` command and expected output at the end of the prompt. This is the single highest-leverage habit in AI-assisted coding: give the agent something to run that proves the thing works. Without it, the agent finishes and declares success — and *you* become the verification loop, manually testing until something breaks. A one-line check at the end of a prompt saves multiple rounds of back-and-forth.
