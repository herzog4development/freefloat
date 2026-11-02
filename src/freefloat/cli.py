"""Print the top N companies by estimated free-float market cap."""
from __future__ import annotations

import argparse
import json
from importlib import resources

from freefloat.scraper import fetch_html, parse_companies

SCAN_DEPTH = 30  # companies scanned; a low-float giant can still fall out of the top 3


def load_float_factors() -> dict[str, float]:
    text = resources.files("freefloat").joinpath("float_factors.json").read_text()
    return {k: v for k, v in json.loads(text).items() if not k.startswith("_")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", type=int, default=3, help="how many companies to show")
    args = parser.parse_args()

    html, fetched_at = fetch_html()
    companies = parse_companies(html)[:SCAN_DEPTH]
    if not companies:
        raise SystemExit("No companies parsed - the site layout may have changed.")

    factors = load_float_factors()
    rows = []
    for c in companies:
        factor = factors.get(c.ticker)
        rows.append((c, factor if factor is not None else 1.0, factor is None))
    rows.sort(key=lambda r: r[0].market_cap_usd * r[1], reverse=True)

    print(f"Source: companiesmarketcap.com, fetched {fetched_at:%Y-%m-%d %H:%M} UTC")
    print(f"{'#':<3}{'Company':<28}{'Total $T':>10}{'Float':>8}{'Free-float $T':>15}")
    for i, (c, f, assumed) in enumerate(rows[: args.n], 1):
        flag = "  (float unknown, assumed 1.0)" if assumed else ""
        print(
            f"{i:<3}{c.name[:27]:<28}{c.market_cap_usd / 1e12:>10.2f}"
            f"{f:>8.2f}{c.market_cap_usd * f / 1e12:>15.2f}{flag}"
        )
    print("\nNote: float factors are assumptions in float_factors.json, not scraped data.")


if __name__ == "__main__":
    main()
