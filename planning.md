# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I chose Computer Science professor and course reviews from Hunter College CUNY. This knowledge is highly valuable because official university course catalogs only show generic course descriptions, completely hiding realities like harsh grading, hidden assignment rules, or professors who do not provide study materials. Access to these raw peer reviews allows students to navigate unhelpful teaching styles, prepare for unexpected workloads, and actually survive the major.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate My Professors |Reviews for Prof. Yi |https://www.ratemyprofessors.com/professor/2634841 |
| 2 |Rate My Professors |Reviews for Prof. Epstein |https://www.ratemyprofessors.com/professor/192300 |
| 3 |Rate My Professors |Reviews for Prof. Shostak|https://www.ratemyprofessors.com/professor/1823870 |
| 4 |Rate My Professors |Reviews for Prof. Oyekoya |https://www.ratemyprofessors.com/professor/2558461 |
| 5 |Rate My Professors |Reviews for Prof. St. John |https://www.ratemyprofessors.com/professor/2324096 |
| 6 |Rate My Professors |Reviews for Prof. Shankar |https://www.ratemyprofessors.com/professor/257190 |
| 7 |Rate My Professors |Reviews for Prof. Tojeira |https://www.ratemyprofessors.com/professor/1660967 |
| 8 |Rate My Professors |Reviews for Prof. Naing |https://www.ratemyprofessors.com/professor/2693848 |
| 9 |Rate My Professors |Reviews for Prof. Schweitzer |https://www.ratemyprofessors.com/professor/257192 |
| 10 |Rate My Professors |Reviews for Prof. Mneimneh |https://www.ratemyprofessors.com/professor/926045 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 600 characters

**Overlap:** 150 characters

**Reasoning:** Rate My Professors data consists of short, independent student reviews. A chunk size of 600 characters keeps individual reviews intact without mixing unrelated reviews for the same professor. The 150-character overlap prevents critical facts (like specific quiz grading weights or course numbers) from being clipped across boundary lines.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 4 chunks per query

**Production tradeoff reflection:** If deploying for real users without cost constraints, I would evaluate models like OpenAI's `text-embedding-3-large` to leverage a larger context window and better semantic nuance. However, a cloud API introduces external dependencies, financial costs per token, and higher network latency compared to running `all-MiniLM-L6-v2` locally and free of charge.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |How much of the final grade do pop quizzes account for in Eric Schweitzer's CS265 class? |Pop quizzes account for 60% of the final grade. |
| 2 |Does Professor Shankar post his handwritten lecture notes or homework answers online for CSCI260? |No, he does not post his handwritten notes or homework answers on Brightspace. |
| 3 |What specific grading criteria does Professor Shostak look for on his CS340 exams? |He is very strict and looks for specific words, terms, and memorized definitions. |
| 4 |What software tool must students teach themselves to use for the CSCI49383 VR development class projects? |Students must teach themselves to use Unity. |
| 5 |What resources or grading adjustments does Professor Saad provide to help students pass his difficult CSCI150 class? |He provides generous curves and extra credit opportunities in recitation. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Noisy Text Data: The copied reviews contain boilerplate and meta-labels like "Quality", "Difficulty", and "Thumbs up/down". This numerical noise can pollute semantic search results if not handled or filtered during ingestion.

2. Context Fragmentation: A student's thought might span multiple lines, risking an unnatural split where a professor's name or specific class code is isolated from the actual critique in an adjacent chunk.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```mermaid
graph TD
    A[Document Ingestion: Local .txt files] --> B[Chunking: Character Split 600/150]
    B --> C[Embedding & Vector Store: all-MiniLM-L6-v2 + ChromaDB]
    C --> D[Retrieval: Semantic Similarity Top-4]
    D --> E[Generation: Groq llama-3.3-70b-versatile]
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I will use Copilot. I will feed it the Chunking Strategy section and ask for a Python script that reads all .txt files from our data folder and applies a character split. I will verify it by printing out 5 sample chunks to check that the metadata (source filename) is preserved and the characters don't cut off mid-thought unnecessarily.

**Milestone 4 — Embedding and retrieval:** I will use Copilot. I will hand it the Retrieval Approach parameters and ask it to build a local vector database initialization using ChromaDB and sentence-transformers. I will verify the output by submitting 3 sample queries and manually checking if the distance scores are under 0.5 and the content matches the intent.

**Milestone 5 — Generation and interface:** I will use Copilot. I will supply the full prompt requirements along with the Evaluation Plan questions to generate an end-to-end processing script connecting ChromaDB to the Groq API. I will request a minimal Gradio block UI interface. I will verify grounding by asking an out-of-scope question to ensure the system gracefully refuses to answer instead of hallucinating.
