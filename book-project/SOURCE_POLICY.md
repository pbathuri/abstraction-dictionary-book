# SOURCE POLICY — Acquisition, Scoring, and Citation Standards

## Principles

1. Every substantive technical claim must have provenance.
2. No fabricated citations, URLs, paper titles, or author attributions.
3. Sources are scored by trust tier and recency.
4. The research corpus must be reproducible from source manifests and snapshots.

## Source Types

| Type | Description | Examples |
|------|-------------|---------|
| **Official documentation** | Published docs from model/tool providers | OpenAI docs, Anthropic docs, HuggingFace docs |
| **Peer-reviewed research** | Published papers with DOI or arXiv ID | Attention Is All You Need, chain-of-thought papers |
| **Technical blog posts** | Engineering blogs from credible organizations | OpenAI blog, Google AI blog, Anthropic research |
| **Benchmark results** | Published evaluation results with methodology | MMLU, HumanEval, published leaderboards |
| **Open educational content** | Courses, tutorials, guides with named authors | Stanford CS courses, Prompt Engineering Guide |
| **Community knowledge** | Well-sourced discussions, established practices | High-quality Stack Overflow, established GitHub repos |
| **Original observation** | Empirically verified by our pipeline | Our own eval results, reproducible experiments |

## Trust Tiers

| Tier | Label | Criteria | Usage |
|------|-------|----------|-------|
| T1 | **High trust** | Peer-reviewed, official docs, published benchmarks | May be cited as primary evidence |
| T2 | **Moderate trust** | Named-author blog posts from credible orgs, established guides | May be cited with attribution |
| T3 | **Low trust** | Anonymous posts, undated content, single-source claims | May inform research but not cited as sole evidence |
| T4 | **Unverified** | No author, no date, no institutional backing | Not citable; flag for replacement |

## Source Card Schema

Every acquired source produces a source card stored in `corpus/source_cards/`.

```json
{
  "source_id": "src_001",
  "title": "",
  "url": "",
  "author": "",
  "organization": "",
  "date_published": "",
  "date_accessed": "",
  "source_type": "",
  "trust_tier": "T1|T2|T3|T4",
  "extraction_method": "scrapling|manual|api",
  "content_hash": "",
  "snapshot_path": "",
  "normalized_path": "",
  "extraction_notes": "",
  "topics": [],
  "key_claims": []
}
```

## Citation Format

In-entry citations use bracketed source IDs: `[src_001]`

Full citation details live in the entry's `.sources.json` file.

In the final compiled book, citations resolve to a numbered bibliography in Appendix format.

## Acquisition Rules

1. **Snapshot everything.** Raw HTML/content is stored in `corpus/raw/` with timestamp.
2. **Normalize to markdown.** Clean extractions go to `corpus/normalized/`.
3. **Never modify source text.** Normalization is structural (stripping nav, ads, boilerplate), never content-altering.
4. **Respect robots.txt and rate limits.** Scrapling fetchers must honor site policies.
5. **No paywalled content.** Only publicly accessible sources.
6. **Date all sources.** If a source has no visible date, record "undated" and assign T3 or T4.

## Staleness Rules

- Documentation: refresh if older than 6 months
- Blog posts: acceptable up to 2 years if the technical content remains accurate
- Benchmarks: refresh if a new major evaluation has been published
- Research papers: no staleness limit for established results; flag if superseded

## Claim Verification

Before an entry reaches `final/` status:
1. Every technical claim must map to at least one source_id
2. Claims with only T3/T4 sources must be flagged `[NEEDS_STRONGER_SOURCE]`
3. Claims about model capabilities must cite specific documentation or published benchmarks
4. Claims about parameter counts must cite the model's official release announcement
5. If no public parameter count exists, use tier classification instead
