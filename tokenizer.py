import re
import keyword

PYTHON_KEYWORDS = set(keyword.kwlist)

TOKEN_PATTERN = re.compile(r"""
    (?P<COMMENT>\#.*)
  | (?P<STRING>'[^']*'|"[^"]*")
  | (?P<NUMBER>\b\d+\.?\d*\b)
  | (?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<OP>[^\sA-Za-z0-9_])
""", re.VERBOSE)


def tokenize_with_lines(code: str) -> list[tuple[str, int]]:
    """
    Same normalization as before (VAR, NUM, STR, keywords, operators),
    but each token is paired with the line number it came from.
    This lets us trace a matched token back to a real line in the source.
    """
    result = []
    for line_num, line in enumerate(code.splitlines(), start=1):
        for match in TOKEN_PATTERN.finditer(line):
            kind = match.lastgroup
            value = match.group()

            if kind == "COMMENT":
                continue
            elif kind == "STRING":
                result.append(("STR", line_num))
            elif kind == "NUMBER":
                result.append(("NUM", line_num))
            elif kind == "IDENTIFIER":
                if value in PYTHON_KEYWORDS:
                    result.append((value, line_num))
                else:
                    result.append(("VAR", line_num))
            elif kind == "OP":
                result.append((value, line_num))

    return result


def tokenize(code: str) -> list[str]:
    """Backward-compatible: just the tokens, no line numbers."""
    return [tok for tok, _ in tokenize_with_lines(code)]


if __name__ == "__main__":
    sample = """
def calculate_total(price, quantity):
    # returns total cost
    total = price * quantity
    if total > 100:
        return total * 0.9
    return total
"""
    for tok, line in tokenize_with_lines(sample):
        print(f"line {line}: {tok}")