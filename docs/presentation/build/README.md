# Building `bao-cao-lan-1.pptx`

The deck fills `docs/presentation/template-vi.pptx` (Slidesgo template — not redistributed here; download it from Slidesgo and keep its credits slide)
through ppt-master's Edit Native PPTX route.

```bash
S=.claude/skills/ppt-master/scripts; W=runs/slides/bao-cao-lan-1_20261108
python3 $S/pptx_to_svg.py docs/presentation/template-vi.pptx -o $W --inheritance-mode both --roundtrip   # once
python3 docs/presentation/build/build_bao_cao_lan_1.py          # rebuild 20 pages from pristine imports
python3 $S/svg_authoring_view.py $W/authoring-svg-flat --refresh-summary
python3 $S/svg_quality_checker.py $W --roundtrip --json         # must report 0 errors
python3 $S/svg_to_pptx.py $W --roundtrip                        # writes $W/exports/*.pptx
```

Numbers on slides come from `data/` (rq2_ours.csv, rq3_bugsinpy.csv, rq3_renamed.csv, rq3_families.csv,
rq_decomposition.csv, semfault_verified_gt.json, llm_cost.csv) and the figure from
`docs/report/generated/pareto.pdf`; run `scripts/regenerate_all.sh` first. Needs `pdftoppm` (poppler). Fonts: the template uses Be Vietnam Pro and IBM Plex Mono — install
them on the presenting machine.
