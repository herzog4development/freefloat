from freefloat.scraper import parse_companies

SAMPLE = """
<table><tbody>
<tr><td>1</td>
  <td class="name-td"><div class="name-div"><div class="company-name">Apple</div>
  <div class="company-code">AAPL</div></div></td>
  <td class="td-right" data-sort="5029000000000">$5.029 T</td></tr>
<tr><td>2</td>
  <td class="name-td"><div class="name-div"><div class="company-name">NVIDIA</div>
  <div class="company-code">NVDA</div></div></td>
  <td class="td-right" data-sort="4941000000000">$4.941 T</td></tr>
</tbody></table>
"""


def test_parse_companies():
    result = parse_companies(SAMPLE)
    assert [c.ticker for c in result] == ["AAPL", "NVDA"]
    assert result[0].market_cap_usd == 5.029e12
