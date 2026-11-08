# Building `bao-cao-lan-1.pptx`

The deck fills `docs/presentation/template-vi.pptx` (Slidesgo template — not redistributed here; download it from Slidesgo and keep its credits slide)
through ppt-master's Edit Native PPTX route.

```bash
S=.claude/skills/ppt-master/scripts; W=runs/slides/bao-cao-lan-1_20261108
python3 $S/pptx_to_svg.py docs/presentation/template-vi.pptx -o $W --inheritance-mode both --roundtrip   # once
python3 docs/presentation/build/build_bao_cao_lan_1.py          # rebuild 18 pages from pristine imports
python3 $S/svg_authoring_view.py $W/authoring-svg-flat --refresh-summary
python3 $S/svg_quality_checker.py $W --roundtrip --json         # must report 0 errors
python3 $S/svg_to_pptx.py $W --roundtrip                        # writes $W/exports/*.pptx
```

Numbers on slides come from `data/` (rq1a_table.csv, semfault_labels.csv, bugsinpy_status.csv,
pilot_dev_gemini_default.csv). Fonts: the template uses Be Vietnam Pro and IBM Plex Mono — install
them on the presenting machine.
