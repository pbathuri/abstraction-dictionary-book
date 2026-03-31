# compare

> Place two or more items side by side and map both their similarities and their differences along specified dimensions.

## The Scene

Your team is choosing between three state management approaches for a React app with 200+ components. You ask the model: "Tell me about Redux Toolkit, Zustand, and React Context." You get three encyclopedia entries. Accurate, comprehensive, useless for making a decision.

You rewrite: "Compare Redux Toolkit, Zustand, and React Context + useReducer along five dimensions: boilerplate for a new state slice, DevTools experience, performance with frequent updates, learning curve for a Redux-familiar team, and unit test ergonomics. For each dimension, state which option is strongest and why. Output as a table."

Now you have a decision artifact. The difference isn't just specificity — it's the activation of *contrastive reasoning*, a fundamentally different cognitive mode from description.

## What This Actually Is

Comparison forces parallel analysis. You can't compare two items without implicitly constructing a set of dimensions along which both are measured. This is what makes it more powerful than description — description looks at one thing; comparison looks at the *space between* things, and that's where insight lives.

"Compare" activates a specific model behavior: interleaved analysis, moving between items dimension by dimension. The model doesn't write about Item A then Item B. It writes about A *in relation to* B. When this works, the output reads like a dialogue between the items. When it fails, it reads like two summaries stapled together.

The quality depends entirely on whether dimensions are explicit. "Compare Python and Rust" lets the model pick generic axes. "Compare Python and Rust for memory safety, onboarding time for Java developers, and latency-sensitive microservices" produces something you didn't already know.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Tell me about Postgres and MySQL" | "Compare Postgres and MySQL for a read-heavy analytics workload with 50 concurrent users" | Activates contrastive reasoning instead of encyclopedic retrieval |
| "Compare X and Y" | "Compare X and Y along these dimensions: [list]. For each, state which is stronger." | Explicit axes prevent generic output |
| "What's the difference?" | "Contrast the architectural philosophies, not just the feature lists" | Pushes past surface-level to structural differences |
| "Which is better?" | "Compare on these criteria, score 1-5 each, then state which scores highest overall" | Structured judgment beats a vague recommendation |
| (prose comparison) | "Output as a markdown table with a summary paragraph below" | Tables force parallel structure by format |

## Before → After

**Before:**
```
Compare PostgreSQL and MongoDB.
```

**After:**
```
Compare PostgreSQL and MongoDB for a write-heavy IoT data
ingestion pipeline processing 100,000 events per second.

Dimensions: write throughput, schema flexibility, operational
complexity, and cost at scale.

For each dimension, state which option is stronger and why.
Be direct — do not hedge to appear balanced.
```

**What changed:** Context (the specific use case) plus explicit dimensions plus permission to be direct. The model can't retreat into "it depends" because the scenario is concrete.

## Try This Now

```
Compare these two prompt styles for asking a model to write
a product description:

STYLE A: "Write a product description for a travel mug.
Make it sound good."

STYLE B: "Write a product description for a ceramic travel mug.
Audience: design-conscious millennials on Etsy. Tone: warm,
slightly witty. Length: 50 words. Must mention: handmade,
dishwasher-safe, 12oz."

Compare them along three dimensions:
1. How much the model has to guess
2. Consistency across 10 generations
3. Quality ceiling (best possible output)

Use a table. Be blunt about which is better on each dimension.
```

## When It Breaks

- **Compare without dimensions** → The model defaults to generic axes (cost, popularity, ease of use) that tell you nothing. Always specify at least 2-3 axes.
- **Compare as sequential description** → Three paragraphs about X, then three about Y, with no analytical intersection. Fix: "Analyze each dimension for both items together, not sequentially." Or force a table.
- **False symmetry** → The model forces both items to appear equally good and bad — a politeness artifact from training. Fix: "Be direct about which is stronger on each dimension. Do not hedge to appear balanced."

## Quick Reference

- Family: instructional action
- Adjacent: → contrast (differences only), → evaluate (adds judgment), → analyze (internal structure of one item)
- Model fit: Comparison is well-handled across tiers. Table-format outputs are more reliable than prose across all models. Small models degrade on 3+ items — they lose track of the third.
