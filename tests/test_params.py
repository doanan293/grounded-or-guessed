import json

import pytest

from flx import params


def _csv(tmp_path, prm):
    f = tmp_path / "s.csv"
    f.write_text("gt,config,variant,params\n"
                 f'repaired,semloc_gemini_T0.8,covgate,"{json.dumps(prm).replace(chr(34), chr(34) * 2)}"\n'
                 'repaired,semloc_gemini_T0.8,semloc,"{}"\n')
    return f


def test_chosen_params_keeps_every_covgate_knob(tmp_path):
    prm = {"gate": False, "lam": 0.5, "no_prior": False, "grounded_prior": True}
    got = params.chosen_params("repaired", path=_csv(tmp_path, prm))
    assert got == prm and got["grounded_prior"] is True


def test_chosen_params_unknown_gt_raises(tmp_path):
    with pytest.raises(KeyError):
        params.chosen_params("original", path=_csv(tmp_path, {"gate": False, "lam": 0.0, "no_prior": False,
                                                              "grounded_prior": False}))
