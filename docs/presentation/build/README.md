# Building the decks (`bao-cao-lan-1/2.pptx`, `bao-ve.pptx`)

The deck fills `docs/presentation/template-vi.pptx` (Slidesgo template — not redistributed here; download it from Slidesgo; the CREDITS line on the last page is removed from the exported deck by `strip_credits.py`)
through ppt-master's Edit Native PPTX route. `make_decks.sh [lan1] [lan2] [baove]` builds, checks and exports
them; each progress report shows a little more than the one before (lần 1, 18–19/11 = group, work split, AI tools, RQ1,
main comparison, status; lần 2, 25–26/11 = + RQ3, contributions, status; bảo vệ = everything).

Lần 1 is a storytelling deck (`story.py`: one claim per page as the title, one native-SVG picture from `viz.py` as the
evidence); its cover carries the Vietnamese title large and the English paper title small, never mixed.

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
