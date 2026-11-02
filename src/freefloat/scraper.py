"""Fetch the market-cap table from companiesmarketcap.com."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

URL = "https://companiesmarketcap.com/"
USER_AGENT = "free-float-top3-helloworld/0.1 (personal learning project)"


@dataclass(frozen=True)
class Company:
    name: str
    ticker: str
    market_cap_usd: float


def fetch_html(url: str = URL) -> tuple[str, datetime]:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    return resp.text, datetime.now(timezone.utc)


def parse_companies(html: str) -> list[Company]:
    """Parse rows of the main ranking table (total, not free-float, market cap)."""
    soup = BeautifulSoup(html, "html.parser")
    companies: list[Company] = []
    for row in soup.select("table tbody tr"):
        name_el = row.select_one(".company-name")
        code_el = row.select_one(".company-code")
        if not name_el:
            continue
        # The market cap cell carries the raw USD value in data-sort.
        cap = None
        for td in row.find_all("td"):
            raw = td.get("data-sort")
            if raw and re.fullmatch(r"\d{9,}", raw):
                cap = float(raw)
                break
        if cap is None:
            continue
        companies.append(
            Company(
                name=name_el.get_text(strip=True),
                ticker=code_el.get_text(strip=True) if code_el else "",
                market_cap_usd=cap,
            )
        )
    return companies
