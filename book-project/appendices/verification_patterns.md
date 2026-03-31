# Appendix D: Verification Patterns

> Structured approaches for checking AI outputs before accepting them.

## Pattern 1: Rubric-Based Verification

```
Evaluate the output against this rubric:
1. [CRITERION_A]: Does the output [SPECIFIC_CHECK]? (Yes/No/Partial)
2. [CRITERION_B]: Does the output [SPECIFIC_CHECK]? (Yes/No/Partial)
3. [CRITERION_C]: Does the output [SPECIFIC_CHECK]? (Yes/No/Partial)

Score: count of Yes answers / total criteria
Accept if score >= [THRESHOLD]
```

## Pattern 2: Self-Critique Loop

```
Step 1: Produce the output.
Step 2: Review your output and identify:
  - Claims that lack evidence
  - Logical gaps
  - Assumptions that were not stated
Step 3: Revise to address each identified issue.
Step 4: If any issues remain unresolvable, flag them explicitly.
```

## Pattern 3: Adversarial Check

```
After producing your response, attempt to find:
1. A counterexample that contradicts your main claim
2. An edge case where your recommendation fails
3. An alternative interpretation of the same evidence
If any succeed, revise your response to acknowledge them.
```

## Pattern 4: Citation Audit

```
For each factual claim in your output:
1. Identify the source
2. If no source exists, mark the claim as [UNVERIFIED]
3. If the source is older than [N] months, mark as [NEEDS_REFRESH]
4. Return a summary of claim coverage
```

## Pattern 5: Consistency Cross-Check

```
Compare your output against [REFERENCE_DOCUMENT].
Flag any:
- Contradictions with the reference
- Terms used differently than in the reference
- Claims that the reference does not support
```

## Pattern 6: Output-Schema Validation

```
Verify that your output matches the required schema:
- All required fields are present
- Field types are correct (string, number, list)
- Field lengths are within bounds
- No extra fields are included
Return a validation report.
```

*Each pattern maps to entries in Part II. See → rubric, → verification loop, → falsifiability, → audit trail.*
