"""Remove the template's CREDITS line from the exported deck (the group asked to drop it). The line lives on a shared
Layout, which the round-trip exporter must not edit, so it is removed from the finished PPTX instead.
    python3 strip_credits.py deck.pptx"""
import sys

from pptx import Presentation

path = sys.argv[1]
prs = Presentation(path)
removed = 0
layouts = {id(s.slide_layout._element): s.slide_layout for s in prs.slides}
for layout in layouts.values():
    for shape in list(layout.shapes):
        if shape.has_text_frame and "CREDITS" in shape.text_frame.text:
            shape._element.getparent().remove(shape._element)
            removed += 1
prs.save(path)
print(f"{path}: removed {removed} credits shape(s)")
