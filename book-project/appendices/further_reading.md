# Appendix F: Further Reading

> A curated list of recommended sources for readers who want to go deeper on the topics covered in this book, organized by area of study.

---

## How This List Is Organized

Sources are grouped by topic area, not by format. Each section includes a mix of academic papers, technical documentation, and practitioner resources. We have prioritized sources that are freely available, actively maintained, and directly relevant to the abstractions in Part II. Where a source informed a specific family of entries, we note the connection.

This is not an exhaustive bibliography (see the Bibliography appendix for full citations of works referenced in entries). This is a starting-point reading list for readers who want to build deeper expertise in the areas this book touches.

---

## Foundations of Prompt Engineering

The essential papers and guides for understanding how prompts work and why certain patterns are effective.

- **Schulhoff et al. (2025), "The Prompt Report"** — The most comprehensive taxonomy of prompting techniques as of publication. Essential for understanding the full landscape of methods, from zero-shot to multi-agent. Directly informed the Instructional Action and Quality Control families.
- **Sahoo et al. (2025), "A Systematic Survey of Prompt Engineering"** — Strong complement to The Prompt Report with deeper coverage of application-specific techniques. Useful for readers interested in domain-adapted prompting.
- **Wei et al. (2022), "Chain-of-Thought Prompting"** — The foundational paper on reasoning chains in prompts. Required reading for understanding → decomposition, → hierarchy, and → justify.
- **White et al. (2023), "A Prompt Pattern Catalog"** — Organized catalog of reusable prompt structures. Useful as a practitioner companion to this book's more abstract vocabulary.
- **OpenAI Prompt Engineering Guide** (https://platform.openai.com/docs/guides/prompt-engineering) — Continuously updated practical guidance. The best starting point for readers new to structured prompting.
- **Anthropic Prompt Engineering Documentation** (https://docs.anthropic.com/) — Particularly strong on constitutional AI principles, harmlessness constraints, and long-context strategies.

## Vocabulary, Rhetoric, and Language Precision

For readers interested in the linguistic foundations underlying the Core Abstraction and Tone/Style families.

- **Schreiter (2024), "Prompt Engineering: How Prompt Vocabulary Affects Domain Knowledge"** — The key empirical study on how word choice in prompts affects model performance. Directly shaped entries on → specificity, → precision, and → register.
- **Grice, H. P. (1975), "Logic and Conversation"** — The foundational work on conversational maxims (quantity, quality, relation, manner). The principles map directly to specificity, relevance, and clarity in prompt design.
- **Williams, J. M. & Bizup, J., *Style: Lessons in Clarity and Grace*** — The best general guide to clear, precise writing. Relevant to every entry in the Tone/Style family and to prompt clarity generally.
- **Lanham, R. A., *Revising Prose*** — The "paramedic method" for cutting verbal fat. Directly relevant to → terseness and → signal-to-noise ratio.

## Context Engineering and Long-Context Strategies

For readers building systems that manage information across turns, documents, and agents.

- **Lewis et al. (2020), "Retrieval-Augmented Generation"** — The foundational RAG paper. Essential for understanding → retrieval scaffolding and → source anchoring.
- **Gao et al. (2023), "Retrieval-Augmented Generation for Large Language Models: A Survey"** — Comprehensive survey of RAG architectures, retrieval methods, and evaluation. The best single-source overview of the field as of 2024.
- **Xu et al. (2024), "Retrieval Meets Long Context LLMs"** — Examines the interaction between retrieval strategies and expanded context windows. Relevant to → context budget and → context windowing.
- **Anthropic's Long Context Window Guide** — Practical documentation on managing 100K+ token contexts. Directly relevant to the Context Architecture family.

## Agentic Workflows and Multi-Agent Systems

For readers building or designing systems with multiple cooperating AI agents.

- **OpenAI Agents SDK Documentation** (https://openai.github.io/openai-agents-python/) — The reference implementation for delegation, handoff, and tool use patterns. Directly informed the Agent Workflow family and Appendix B patterns.
- **LangGraph Documentation** (https://langchain-ai.github.io/langgraph/) — Graph-based agent orchestration. Particularly relevant to → orchestration, → routing, and → pipeline.
- **Wu et al. (2023), "AutoGen"** — Multi-agent conversation framework with strong coverage of agent cooperation patterns. Relevant to → delegation, → handoff, and → shared state.
- **Hong et al. (2023), "MetaGPT"** — Multi-agent framework using software engineering metaphors. Interesting for its approach to → planner-executor split and role-based delegation.
- **Park et al. (2023), "Generative Agents"** — Simulated societies of AI agents with memory and planning. Relevant to → memory cueing, → shared state, and long-horizon agent behavior.

## Reasoning, Self-Correction, and Verification

For readers interested in how models reason, self-correct, and validate their own outputs.

- **Yao et al. (2023), "Tree of Thoughts"** — Extends chain-of-thought to tree-structured reasoning with backtracking. Relevant to → decomposition and → planner-executor split.
- **Madaan et al. (2023), "Self-Refine"** — Iterative self-improvement without external feedback. Core reference for → verification loop and → feedback loop.
- **Dhuliawala et al. (2023), "Chain-of-Verification"** — Systematic approach to reducing hallucination through structured verification. Directly relevant to → verification loop and → falsifiability.
- **Shinn et al. (2023), "Reflexion"** — Verbal reinforcement learning for language agents. Relevant to → feedback loop and → regression check.
- **Zhou et al. (2022), "Least-to-Most Prompting"** — Progressive decomposition strategy. Key reference for → decomposition and → progressive disclosure.

## Evaluation, Benchmarking, and Quality

For readers who need to measure whether their prompts and agents are actually working.

- **Zheng et al. (2023), "Judging LLM-as-a-Judge"** — On using language models as evaluators. Directly relevant to → rubric, → evaluate, and → critique.
- **Liang et al. (2022), "Holistic Evaluation of Language Models" (HELM)** — The most comprehensive evaluation framework. Useful for understanding what "good output" means across dimensions.
- **Ari (2025), "5C Prompt Contracts"** — Structured framework for prompt reliability. Relevant to → constrain, → rubric, and systematic prompt design.
- **Debnath et al. (2025), "A Comprehensive Survey of Prompt Engineering Techniques"** — Broad survey with coverage of evaluation methods. Useful as a second-opinion reference alongside Schulhoff et al.

## Model Architecture and Capabilities

For readers who want to understand *why* models behave the way they do, without requiring deep ML expertise.

- **Vaswani et al. (2017), "Attention Is All You Need"** — The transformer paper. Understanding attention mechanisms helps explain why context structure matters.
- **Brown et al. (2020), "Language Models are Few-Shot Learners"** — The GPT-3 paper that demonstrated in-context learning. Explains why examples in prompts work.
- **Kojima et al. (2022), "Large Language Models are Zero-Shot Reasoners"** — The "Let's think step by step" paper. Explains the mechanism behind simple reasoning prompts.
- **Anthropic Research Blog** (https://www.anthropic.com/research) — Regularly publishes accessible explanations of model behavior, safety, and capability patterns.

---

*Sources in this appendix are drawn from the project's research corpus and scored at T1 (peer-reviewed or official documentation) or T2 (high-quality preprint or established practitioner resource) trust levels. See SOURCE_POLICY.md for scoring criteria. All URLs verified as of March 2026.*
