# Related work — comparison table

All entries are in `docs/report/references.bib` (BibTeX key in the first column), verified against
doi.org / arXiv on 2026-11-08.

| Key | Work | Year | Group | Signal | Granularity | Benchmark | Difference from our study |
|---|---|---|---|---|---|---|---|
| jones2002 | Tarantula — visualization of test information | 2002 | SBFL | coverage | statement | Siemens | classic coverage formula; baseline only |
| abreu2009 | Practical evaluation of SBFL (Ochiai) | 2009 | SBFL | coverage | block/statement | Siemens, SIR | Ochiai is the formula SemLoc reuses on violations |
| wong2014dstar | DStar | 2014 | SBFL | coverage | statement | SIR programs | stronger coverage formula; our second SBFL baseline |
| wong2016survey | Survey on software fault localization | 2016 | survey | all | — | — | taxonomy for our related-work chapter |
| desouza2016 | SBFL survey: techniques, advances, challenges | 2016 | survey | coverage | — | — | documents tie and omission-fault issues in SBFL evaluation |
| pearson2017 | Evaluating and improving fault localization | 2017 | evaluation | coverage, mutation | statement | Defects4J, artificial faults | real vs artificial faults; omission-fault and tie handling — basis for our evaluation audit |
| papadakis2015 | Metallaxis-FL | 2015 | MBFL | mutation | statement | Siemens | mutation instead of coverage; not evaluated |
| moon2014 | MUSE: ask the mutants | 2014 | MBFL | mutation | statement | SIR | mutation-based; not evaluated |
| zeller2002tse | Delta debugging: simplifying failure-inducing input | 2002 | reduction | input/program reduction | input | — | DD baseline in SemLoc's table |
| zeller2002chains | Cause-effect chains | 2002 | reduction | program state | state | — | causal view behind counterfactual verification |
| ernst2007daikon | Daikon likely invariants | 2007 | invariants | inferred invariants | program point | — | SemLoc's constraints are LLM-inferred invariants; Daikon infers them from traces |
| kang2024autofl | AutoFL — LLM explainable FL | 2023 | LLM FL | LLM + tool calls | method | Defects4J, BugsInPy | function level; SemLoc uses it as RQ3 backbone |
| qin2025agentfl | AgentFL — project-level LLM FL | 2024 | LLM FL | LLM agents | method | Defects4J | multi-agent, Java, function level |
| xu2025flexfl | FlexFL — open-source LLM FL | 2024 | LLM FL | LLM + SBFL hints | method | Defects4J, GHRB | combines SBFL output with LLMs — closest idea to CovGate, but at method level |
| yang2026semloc | SemLoc | 2026 | LLM FL | LLM constraints + execution | statement | SemFault-250, BugsInPy (7) | the method we reproduce and extend |
| yang2026effiholmes | EffiHolmes | 2026 | perf FL | differential profiling + LLM | file/function | RepoEffi-Bench (140) | performance faults; same "contrast two executions" idea |
| medeiros2026crash | Crash report mining + LLMs (industrial) | 2026 | LLM FL/APR | stack traces + rankings | file/method | 38 industrial Java crash bugs | industrial evidence that mined rankings help LLMs |
| just2014 | Defects4J | 2014 | benchmark | — | — | Java real faults | Java; we use Python benchmarks |
| widyasari2020 | BugsInPy | 2020 | benchmark | — | — | 493 Python real bugs | our real-bug source for RQ3(a) |
| lin2017quixbugs | QuixBugs | 2017 | benchmark | — | — | 40 programs (Python/Java) | optional extra benchmark |
| sallou2024 | Threats of using LLMs in SE | 2023 | LLM validity | — | — | — | contamination / reproducibility threats we address |
| ramos2024memorize | Are LLMs memorizing bug benchmarks? | 2024 | LLM validity | — | — | Defects4J, BugsInPy, … | evidence of benchmark memorization → our renamed variants (RQ3b) |
| xu2024contam | Benchmark data contamination survey | 2024 | LLM validity | — | — | — | mitigation strategies (rewriting/renaming) |
