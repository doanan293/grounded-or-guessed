# Building the decks (`slide-lan-1/2/3.pptx`, `slide-bao-ve.pptx`)

The deck fills `docs/presentation/template-vi.pptx` (Slidesgo template — not redistributed here; download it from Slidesgo; the CREDITS line on the last page is removed from the exported deck by `strip_credits.py`)
through ppt-master's Edit Native PPTX route. `make_decks.sh [lan1] [lan2] [lan3] [baove]` builds, checks and exports
them. There are three progress talks before the defence, each telling the past week's work (no dates on the slides):
lần 1 = studying the problem and reproducing SemLoc (background, SemLoc step by step, the four RQs, the bonus and the
label problems); lần 2 = fixing the labels and proposing FailLoc (normalization, FailLoc and its flow on example 1,
SemLoc−Bonus, design, main comparison, label review); lần 3 = robustness and contributions (ablation, additions and the
FailLoc+Cov flow, RQ4, cost, contributions); bảo vệ = everything, 28 pages, no progress part.

Every deck builds the pages of every story module (`story_lan1/2/3.py`, `story_flow.py`, `story_baove.py`); the
`LAN1/LAN2/LAN3/BAOVE` lists decide which pages a deck shows. Each page is one claim as the title and one native-SVG
picture from `viz.py` as the evidence; the cover carries the Vietnamese title large and the English paper title small,
never mixed. `tests/test_deck_text.py` checks that no progress talk shows a later talk's work and that the three
progress decks share no content page.

```bash
S=.claude/skills/ppt-master/scripts; W=runs/slides/bao-cao-lan-1_20261108
python3 $S/pptx_to_svg.py docs/presentation/template-vi.pptx -o $W --inheritance-mode both --roundtrip   # once
python3 docs/presentation/build/build_deck.py lan1              # rebuild the pages from pristine imports
python3 $S/svg_authoring_view.py $W/authoring-svg-flat --refresh-summary
python3 $S/svg_quality_checker.py $W --roundtrip --json         # must report 0 errors
python3 $S/svg_to_pptx.py $W --roundtrip                        # writes $W/exports/*.pptx
```

Numbers on slides come from `data/` (rq2_ours.csv, rq3_bugsinpy.csv, rq3_renamed.csv, rq3_families.csv,
rq_decomposition.csv, semfault_verified_gt.json, llm_cost.csv) and the figure from
`docs/report/generated/pareto.pdf`; run `scripts/regenerate_all.sh` first. Needs `pdftoppm` (poppler). Fonts: the template uses Be Vietnam Pro and IBM Plex Mono — install
them on the presenting machine.
