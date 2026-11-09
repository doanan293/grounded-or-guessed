# Offline reproduction image: unit tests, and every table/figure from the archived runs (no LLM, no network at run time).
#   docker build -t grounded-or-guessed .
#   docker run --rm grounded-or-guessed                                   # test suite
#   docker run --rm -v $PWD/dist:/dist grounded-or-guessed bash -c \
#     "tar xzf /dist/grounded-or-guessed-runs-*.tar.gz && scripts/regenerate_all.sh"   # rebuild data/ and tables
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv==0.5.11
WORKDIR /work
COPY . .
RUN uv venv .venv && uv pip install --python .venv/bin/python -e ".[dev]" -e third_party/semloc
ENV PATH="/work/.venv/bin:$PATH" FLX_LLM_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1
CMD ["pytest", "-q"]
