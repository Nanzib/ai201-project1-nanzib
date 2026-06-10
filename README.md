# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
I chose Computer Science professor and course reviews from Hunter College CUNY. This knowledge is highly valuable because official university course catalogs only show generic course descriptions, completely hiding realities like harsh grading, hidden assignment rules, or professors who do not provide study materials. Access to these raw peer reviews allows students to navigate unhelpful teaching styles, prepare for unexpected workloads, and actually survive the major.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/2634841 |
| 2 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/192300 |
| 3 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/1823870 |
| 4 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/2558461 |
| 5 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/2324096 |
| 6 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/257190 |
| 7 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/1660967 |
| 8 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/2693848 |
| 9 | Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/257192 |
| 10| Rate My Professors | Web Text Export | https://www.ratemyprofessors.com/professor/926045 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 600 characters

**Overlap:** 150 characters

**Why these choices fit your documents:** Student reviews are brief, self-contained, and highly dense with distinct opinions. A small character size ensures that individual professor reviews stay unified in single vectors without getting diluted by unrelated reviews for other courses. The 150-character overlap acts as an insurance policy to keep course numbers and grading metrics from being accidentally clipped in half on a boundary line.

**Final chunk count:** 49 chunks across all 10 documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Production tradeoff reflection:** Running this local model is fast, costs nothing, and carries zero external API rate limits or network dependencies. If deploying this system for real users where cost wasn't a constraint, I would weigh upgrading to a model like OpenAI's `text-embedding-3-large`. A production model offers a vastly larger context length and deeper semantic accuracy on abstract text, but it introduces ongoing token expenses, third-party reliance, and higher network latency.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** "You are an assistant for 'The Unofficial Guide'. Answer the user's question using ONLY the provided text blocks as context. Do not use external or general knowledge. If the answer cannot be explicitly found in the text blocks below, reply exactly with: 'I don't have enough information on that.' Keep your answer direct, objective, and accurate to the text."

**How source attribution is surfaced in the response:** Source attribution is programmatically isolated outside the LLM's control. When ChromaDB executes a similarity search, the pipeline loops over the returned chunks, extracts the `source` property from the metadata dictionary, and compiles them into a unique set. This ensures that the exact file origins are cleanly rendered inside a dedicated text module in the Gradio user interface, completely protecting the output from LLM hallucination.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How much of the final grade do pop quizzes account for in Eric Schweitzer's CS265 class? | Pop quizzes account for 60% of the final grade. | "I don't have enough information on that." | Relevant | Inaccurate |
| 2 | Does Professor Shankar post his handwritten lecture notes or homework answers online for CSCI260? | No, he does not post his handwritten notes or homework answers on Brightspace. | "I don't have enough information on that." | Relevant | Inaccurate |
| 3 | What specific grading criteria does Professor Shostak look for on his CS340 exams? | He is very strict and looks for specific words, terms, and memorized definitions. | "Professor Shostak looks for specific words/terms in your answers on his exams." | Relevant | Accurate |
| 4 | What software tool must students teach themselves to use for the CSCI49383 VR development class projects? | Students must teach themselves to use Unity. | "Students must teach themselves to use Unity for VR." | Relevant | Accurate |
| 5 | What resources or grading adjustments does Professor Saad provide to help students pass his difficult CSCI150 class? | He provides generous curves and extra credit opportunities in recitation. | "Provides clear lectures/notes, generous curves, extra credit in recitation, and is accessible outside class." | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** How much of the final grade do pop quizzes account for in Eric Schweitzer's CS265 class?

**What the system returned:** "I don't have enough information on that."

**Root cause (tied to a specific pipeline stage):** This failure occurred due to context fragmentation during the mechanical character-chunking phase. The raw source text file mentions "15 quizzes = 60%" in one section, but separates the explicit phrase "pop quizzes" into a completely independent review paragraph. Because our character splitter statically broke these lines into different text chunks, the strict system prompt blocked the LLM from making the inference that general "quizzes" and "pop quizzes" referred to the exact same grading pool.

**What you would change to fix it:** To fix this issue, I would shift away from a rigid character count strategy and implement a semantic or paragraph-based chunking pipeline. Grouping the text by contextual line breaks or entire review blocks would ensure that highly related sentences regarding grading policies stay clustered in a single vector embedding.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The specification locked down our target embedding patterns and mathematical chunk boundaries early in the project lifecycle. This prevented us from getting stuck in endless trial-and-error cycles during the database build, allowing us to build a completely working vector initialization script on our very first run.

**One way your implementation diverged from the spec, and why:** Our final build diverged slightly regarding how environment variables are extracted. To minimize local configuration errors across mixed development terminals on Windows, we adjusted the pipeline initialization script to implement robust manual string extraction loops directly over our local storage paths instead of relying entirely on standard global shell commands.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I fed the AI tool our explicit `Chunking Strategy` rules from `planning.md` alongside our directory tree constraints.
- *What it produced:* It generated a foundational boilerplate skeleton for loading raw folder metrics and breaking down plain text strings through a character sliding window index.
- *What I changed or overrode:* I manually re-architected the logging layers inside the validation block to actively surface individual console diagnostics, forcing it to print 5 structural test samples directly to the terminal shell to fulfill our chunk validation requirements.

**Instance 2**

- *What I gave the AI:* I gave the AI tool our Groq grounding requirements and the sample Gradio layout instructions from the project prompt.
- *What it produced:* It returned an end-to-end user-facing rendering loop linking database lookups directly to an open Groq completion prompt.
- *What I changed or overrode:* I altered the model system constraints to programmatically enforce an unyielding string match match logic ("I don't have enough information on that") on mismatched lookups, stopping the model from generating polite apologetic hallucinations when users ask out-of-scope questions.
