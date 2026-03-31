# framing

> Same facts, different lens. The lens wins every time.

## The Scene

I was building the AI Ethics Coach — a Chrome extension that helps users think through ethical dimensions of their AI projects. The core content was a set of ethical principles: fairness, transparency, accountability, harm reduction. Same principles everywhere. But I needed three prompt variants for three modes the user could select: Socratic, Research, and Lab.

Same content. Three frames. Completely different outputs.

The **Socratic frame** opened with: "You are a philosophy tutor. When the user describes their AI project, do not tell them what's ethical or unethical. Instead, ask questions that force them to discover the tensions themselves. Never give answers. Only give better questions."

The **Research frame** opened with: "You are a research analyst specializing in AI ethics literature. When the user describes their project, map it to published frameworks (EU AI Act, NIST AI RMF, IEEE Ethically Aligned Design). Cite specific sections. Be precise, not preachy."

The **Lab frame** opened with: "You are a red-team engineer. When the user describes their AI project, identify the three most likely ways it could cause harm in production. For each, describe the failure scenario, the affected population, and one mitigation. Be direct. Skip the disclaimers."

All three used the same underlying ethical principles. All three received the same user input. The Socratic frame produced questions that made users uncomfortable in productive ways. The Research frame produced citations I could actually look up. The Lab frame produced failure scenarios that changed how people designed their systems. The *frame* was the product. The facts were just material.

## What This Actually Is

Framing is choosing where to point the telescope. You have the same sky — the same document, the same data, the same problem. But "look for risks" and "look for opportunities" will surface completely different stars. The model doesn't have opinions. It has attention, and framing directs that attention.

It works through three mechanisms. **Role framing** sets who the model is: "You are a defense attorney" produces different analysis than "You are a prosecutor" on the same case. **Task framing** sets the goal: "Summarize" compresses; "Critique" evaluates; "Compare" contrasts. **Contextual framing** sets the backdrop: "This email is from a frustrated long-time customer" changes how every sentence in the email reads, even though you haven't changed the email. Most prompts that produce "generic" output are suffering from frame absence — the model defaulted to "helpful general assistant," which is the wrong frame for everything except being a helpful general assistant.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Analyze this proposal" | "Analyze this proposal as a skeptical investor looking for red flags" | Role frame gives the analysis a specific lens |
| "Summarize the meeting notes" | "Summarize for someone who missed the meeting and needs to make a decision by Friday" | Contextual frame changes what counts as important |
| "Review this code" | "Review this code as a security auditor. Ignore style. Focus only on input validation" | Task frame narrows what "review" means |
| "What do you think?" | "Argue the strongest case against this approach. Then separately, argue the strongest case for it" | Dual-frame forces perspectives the model wouldn't volunteer |
| "Help me with this email" | "You are the recipient of this email. What's unclear? What would make you not respond?" | Perspective flip reframes the entire task |
| "Evaluate the candidate" | "You are a hiring manager who has been burned by overpromisers. Read this resume with that lens" | Experiential frame activates a specific evaluation mode |

**Power verbs for framing:** frame as, view through, approach from, read as if, adopt the lens of, treat this as.

## Before → After

From the AI Ethics Coach — showing how the same ethical principle produces different outputs under different frames:

> **Principle being applied:** "AI systems should be transparent about their limitations."
>
> **Socratic frame output:**
> ```
> "Your chatbot tells users 'I'm an AI assistant.' But does it tell
> them what it can't do? If a user asks your medical chatbot about
> drug interactions, and the model doesn't know — does the user know
> the model doesn't know? What happens in the gap between the user's
> trust and the system's actual capability?"
> ```
>
> **Research frame output:**
> ```
> "This maps to NIST AI RMF GOVERN 1.2: 'Transparency and
> documentation of the AI system's capabilities, limitations, and
> intended uses.' The EU AI Act Article 52 further requires that
> users be informed they are interacting with an AI system, but
> extends this to performance limitations in high-risk categories."
> ```
>
> **Lab frame output:**
> ```
> "Failure scenario: User asks medical chatbot about drug
> interactions for elderly patients. Model confabulates a safe
> combination that is actually contraindicated. No uncertainty
> flag is displayed. Affected population: elderly users with
> multiple prescriptions. Mitigation: Force-display confidence
> scores and add a hard gate that routes pharmacological queries
> to a verified database before responding."
> ```
>
> **Same principle. Three frames. Three completely different tools for the user.**

## Try This Now

Paste this into ChatGPT:

```
I'm going to give you one sentence. Rewrite it three times, each
time through a different frame. Do NOT change the facts — only
change the angle.

Frame 1: As a risk assessor (what could go wrong?)
Frame 2: As an opportunity scout (what could go right?)
Frame 3: As a historian (what does this remind us of?)

Sentence: "Our company is planning to replace the customer support
team's first-response workflow with an AI agent."

After all three, write one sentence explaining what each frame
revealed that the others missed.
```

The point isn't which frame is "right." The point is that no single frame sees the whole picture, and choosing one is a design decision you're making whether you realize it or not.

## From the Lab

We tested the same content delivered through seven different register/frame combinations and measured how outputs changed on structure, vocabulary, and actionability:

![Same Content, Different Register](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Framing accounted for more output variance than any other single prompt variable we tested, including model choice. A well-framed prompt on a mid-tier model outperformed a poorly-framed prompt on a frontier model. The frame is the strongest lever in the toolbox.

## When It Breaks

- **Unexamined default frame** → You didn't set a frame, so the model used "helpful general assistant." That's a frame too — just the least useful one for any specialized task. If you didn't choose a frame, the model chose for you.
- **Frame-task mismatch** → "You are a creative storyteller. Now audit this financial statement." The model either ignores the frame (wasting tokens) or tries to satisfy both (producing a whimsical audit nobody asked for). Frame and task must point in the same direction.
- **Frame without grounding** → "You are an expert in quantum computing" with no quantum computing source material. The frame creates expectations the model can't meet from training data alone. Frames should match the material available, or you're writing → hallucination bait.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → register (the tonal consequence of framing choices), → perspective (what framing produces), → scope (limits how much; framing orients how), → context (provides information; framing provides orientation)
- **Model fit:** Reliable across all tiers. Frontier models hold complex frames (multi-faceted roles, nuanced stances) across long outputs. Small models hold simple frames ("You are a teacher") but lose nuanced ones ("You are a regulatory expert who prioritizes consumer safety over efficiency").
- **Sources:** Tversky & Kahneman (1981), Schulhoff et al. (2025), Debnath et al. (2025) S2A prompting
