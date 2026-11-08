# Integrating Crash Report Mining and LLMs for Bug Localization and Repair: An Industrial Report

Medeiros, Kulesza, Treude, Lucena, Gomes, Coelho, Adachi, Bonifácio (UFRN, SMU, UFPE). arXiv:2609.04483, 2026.

## Problem
Large industrial systems receive thousands of crash reports per week (one system: ~9,200/week).
It is unclear whether LLMs help developers localize and repair crash-report bugs in production.

## Method
Combine crash report mining — **stack-trace clustering** and **ranking of suspicious files and
methods** — with LLM prompts. Retrospective evaluation of 5 LLMs under 4 prompt configurations,
then the best model on the full dataset.

## Evaluation
- 38 crash bugs from two large Java enterprise systems (university management systems in Brazil).
- Manual validation of localization and repair; inter-rater agreement κ = 0.767 (localization),
  0.500 (repair status), 0.583 (fix category).
- Best configuration localizes up to **71%** and correctly repairs **52%** of crash bugs.
- Response analysis: models often drop documentation, add explanations, truncate output (Gemini
  48.75% truncated); adding the suspicious-method ranking raises references to the developer-patched
  method from 76% to 81%.

## Relevance to our study
- Industrial evidence that **mined program evidence (rankings) improves LLM localization** —
  supports giving the LLM structured runtime evidence rather than raw code.
- Shows LLM output must be checked: truncation, format drift and unverified claims are common →
  motivates SemLoc's executable constraints and our "evidence decides" philosophy.
- Not used experimentally (needs industrial data; spec §9).
