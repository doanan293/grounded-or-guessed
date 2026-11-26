"""Words that must not appear on any slide: clipped abbreviations and terms the owner replaced (18/11)."""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "presentation" / "build"))
import build_deck  # noqa: E402
from slidekit import texts  # noqa: E402

pytestmark = pytest.mark.skipif(not build_deck.WS.exists(), reason="slide workspace (runs/slides) not present")
FORBIDDEN = [r"\bCT\b", r"\bCI\b", r"\d k token", r"k token", r"\+thưởng", r"trượt", r"sửa nhãn", r"nhãn đã sửa", r"LLM hỏi thẳng"]
DECK_NAMES = ["lan1", "lan2", "lan3", "baove"]
ORDER = {d: i for i, d in enumerate(DECK_NAMES)}
# word -> first deck allowed to show it outside the progress table (None: never on a slide)
LEAK = {
    "FailLoc+Cov": "lan3", "BugsInPy": "lan3", "đổi tên": "lan3", "Ablation": "lan3", "CovGate": "lan3",
    "FailLoc+Vote": "lan3", "Đóng góp": "lan3",
    "duyệt mù": "lan2", "rà soát": "lan2", "Nhãn đã chuẩn hóa": "lan2", "nhãn đã chuẩn hóa": "lan2",
    "FailLoc+Verify": "baove", "phân loại thất bại": "baove", "Shapley": "lan3", "Chỉ FailLoc+Cov vào top 3": "baove",
    "coverage_only_wins": None,
}


def _pages(deck):
    build_deck.main(deck)
    return {Path(n).stem: " ".join(texts(build_deck.SVG / n)) for _, n in build_deck.PAGES}


@pytest.mark.parametrize("deck", DECK_NAMES)
def test_no_clipped_words(deck):
    for stem, t in _pages(deck).items():
        for pat in FORBIDDEN:
            assert not re.search(pat, t), (deck, stem, pat)


@pytest.mark.parametrize("deck", ["lan1", "lan2", "lan3"])
def test_decks_do_not_leak(deck):
    """Each progress talk shows the past week's work; later work appears only in its progress table and in the four
    research questions (cau_hoi), which are the plan of the whole study."""
    for stem, t in _pages(deck).items():
        if stem.startswith("tien_do") or stem == "cau_hoi":
            continue
        for word, first in LEAK.items():
            if first is None or ORDER[deck] < ORDER[first]:
                assert word not in t, (deck, stem, word)


def test_progress_decks_are_disjoint():
    import story_lan1
    import story_lan2
    import story_lan3
    shared = {"slide_01.svg", "slide_30.svg"}
    a, b, c = ({n for n, _ in L} - shared for L in (story_lan1.LAN1, story_lan2.LAN2, story_lan3.LAN3))
    assert not (a & b) and not (b & c) and not (a & c), (a & b, b & c, a & c)


def test_progress_talks_have_18_to_20_pages():
    """Owner (25/11): lần 2 and lần 3 hold 18–20 pages each."""
    import story_lan2
    import story_lan3
    assert 18 <= len(story_lan2.LAN2) <= 20 and 18 <= len(story_lan3.LAN3) <= 20


@pytest.mark.parametrize("deck", DECK_NAMES)
def test_every_page_has_notes(deck):
    build_deck.main(deck)
    stems = {Path(n).stem for _, n in build_deck.PAGES} - {"slide_30"}
    have = {f.stem for f in (build_deck.WS / "notes").glob("*.md")}
    assert stems <= have, (deck, stems - have)


def test_covers_carry_no_date():
    assert set(build_deck.OCCASION) == set(DECK_NAMES)
    for d in DECK_NAMES:
        assert not re.search(r"\d{1,2}/\d{1,2}|/20\d\d|\d{1,2}–\d{1,2}", build_deck.OCCASION[d]), d


@pytest.mark.parametrize("deck", ["lan1", "lan2", "lan3"])
def test_progress_table_has_no_dates(deck):
    t = next(v for k, v in _pages(deck).items() if k.startswith("tien_do"))
    assert not re.search(r"\d{1,2}/\d{1,2}", t), deck
    assert "Bảo vệ" in t


def test_bugsinpy_title_holds_on_the_metric_it_plots():
    """The BugsInPy slide says FailLoc is highest: true for every bar it draws, including FailLoc+Cov."""
    import story_lan2
    t = _pages("lan3")["bugsinpy"]
    d = story_lan2.mf.rq3_data()["bugsinpy3"]
    assert "FailLoc+Cov" in t and "Acc@3" in t
    assert d["llm_tests"] == max(d.values())


def test_label_tree_counts_add_up():
    """chuan_hoa: the 'no failing test reaches the label' branch must hold exactly GtNotExecutedN programs."""
    import build_deck
    t = _pages("lan2")["chuan_hoa"]
    m = build_deck._m
    import csv
    import json
    ver = {v["program"]: v["status"] for v in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())}
    not_exec = [r["program"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv")) if r["category"] == "not_executed"]
    confirmed_at_label = sum(ver.get(p) == "confirmed" for p in not_exec)
    assert int(m("GtCorrectedN")) + int(m("GtUnverifiableN")) + confirmed_at_label == int(m("GtNotExecutedN"))
    assert "Sửa nhỏ ngay tại nhãn" in t.split("Có test fail")[0]  # the first question is the fix at the label


def test_baove_is_28_pages_and_ends_on_contributions():
    """Defence: 28 pages (SemLoc step pages dropped 25/11); future research sits on the contributions page, no limitations, no separate conclusion (25/11)."""
    import story_baove
    names = [n for n, _ in story_baove.BAOVE]
    assert len(names) == 28 and names[-2] == "dong_gop_2.svg"
    t = _pages("baove")["dong_gop_2"]
    assert "Hướng phát triển" in t and "Hạn chế" not in t


def test_flow_pages_state_the_real_ranks():
    """The three flow pages run each method on a real example and show the ranks the runs actually gave."""
    import json
    import story_common
    va = story_common.examples()["votes_apportion"]
    cr = json.loads((ROOT / "data" / "fig_cov_example.json").read_text())
    t2, t3 = _pages("lan2"), _pages("lan3")
    f = t2["luong_failloc"]
    assert ", ".join(map(str, va["failloc_top5"])) in f and "LLM-Direct" in f
    s = t2["luong_semloc_bonus"]
    assert "26" in s and "1,2" in s and "SemLoc−Bonus" in s and "29" in s
    c = t3["luong_cov"]
    assert "f=4/p=0" in c.replace(" ", "") and "72" in c
    assert ", ".join(map(str, cr["cov_top5"][0][:3])) in c and ", ".join(map(str, cr["failloc_top5"][0][:3])) in c


def test_flow_pages_are_in_the_right_decks():
    import story_baove
    import story_lan2
    import story_lan3
    names = lambda L: [n for n, _ in L]
    l2 = names(story_lan2.LAN2)
    assert l2.index("failloc_vd.svg") == l2.index("luong_failloc.svg") + 1  # the real prompt right after the flow
    assert l2.index("luong_chuan_hoa.svg") == l2.index("chuan_hoa.svg") + 1
    l3 = names(story_lan3.LAN3)
    assert l3.index("shapley.svg") == l3.index("ablation_la_gi.svg") + 1
    assert l3.index("luong_cov.svg") == l3.index("ba_prompt.svg") + 1
    b = names(story_baove.BAOVE)
    assert {"luong_failloc.svg", "luong_semloc_bonus.svg", "luong_cov.svg"} <= set(b) and len(b) == 28
    assert not {"failloc_vd.svg", "failloc_y_tuong.svg", "phuong_phap.svg"} & set(b)


def test_cov_example_names_its_label_set():
    """combine_responses: the coverage gain holds on the normalized label (72) only; the reviewed labels also count the
    if line 71, which FailLoc already ranks first. The page must say so, and must not call it 'ví dụ 2' (blend_orders)."""
    for deck in ("lan3", "baove"):
        c = _pages(deck)["luong_cov"].lower()
        assert "nhãn đã chuẩn hóa" in c and "nhãn đã rà soát" in c and "71" in c, deck
        assert "ví dụ 2" not in c.lower(), deck


def test_lan3_contributions_hold_no_defence_reasoning():
    """'test đủ để gợi ý lỗi nhưng không đủ để chứng minh' rests on FailLoc+Verify, shown only at the defence."""
    assert "chứng minh" not in _pages("lan3")["dong_gop_2"]
    assert "chứng minh" in _pages("baove")["dong_gop_2"]


def test_label_flow_page_runs_on_a_real_example():
    """luong_chuan_hoa: estimate_temperature, original label 69 that no failing test reaches, a one-token fix at line 68
    (the verified record) makes every test pass, so the normalized label is 68."""
    import json
    rec = next(v for v in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
               if v["program"] == "estimate_temperature")
    t = _pages("lan2")["luong_chuan_hoa"]
    assert rec["original"] == [69] and rec["lines"] == [68] and rec["code"].strip() in t
    assert "if not clamp:" in t and "69" in t and "68" in t and "mọi test pass" in t


def test_shapley_page_works_a_real_example():
    """shapley: the formula worked through on SemLoc's measured Acc@1 (normalized labels): v(guess), v(spectrum) =
    SemLoc−Bonus, v(both) = SemLoc; the two parts printed equal the decomposition file."""
    import csv
    dec = next(r for r in csv.DictReader(open(ROOT / "data" / "rq_decomposition.csv"))
               if r["game"] == "semloc" and r["subset"] == "all" and r["gt"] == "repaired" and r["metric"] == "acc1")
    f = lambda v: f"{100 * float(v):.1f}".replace(".", ",")
    t = _pages("lan3")["shapley"]
    assert f(dec["phi_guess"]) in t and f(dec["phi_spectrum"]) in t and f(dec["full"]) in t


@pytest.mark.parametrize("deck", DECK_NAMES)
def test_section_bands_follow_the_agenda_order(deck):
    """The 'Phần k' band of the pages never goes back to an earlier part (agenda order 1 → 5)."""
    parts = []
    for stem, t in _pages(deck).items():
        m = re.search(r"Phần (\d)", t)
        if m and not stem.startswith("muc_luc"):
            parts.append((int(m.group(1)), stem))
    assert [p for p, _ in parts] == sorted(p for p, _ in parts), (deck, parts)


def test_prompt_lines_are_cut_with_an_ellipsis():
    """ba_prompt: a code line too long for its card ends with '…', never in the middle of a word without a mark."""
    t = _pages("lan3")["ba_prompt"]
    assert "* tota " not in t + " " and "weight_  [" not in t
