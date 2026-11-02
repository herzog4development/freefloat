# free-float-top3

Hello-world project: list the companies with the largest free-float market cap.

It scrapes total market caps from [companiesmarketcap.com](https://companiesmarketcap.com/)
(allowed by its robots.txt) and multiplies by a free-float factor.

**Caveat:** the site has no float data. The factors in
`src/freefloat/float_factors.json` are editable assumptions; unlisted tickers default to 1.0
and are flagged. Cross-check against MSCI/FTSE or a terminal for anything serious.

## Run

```
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
freefloat -n 3
pytest
```
