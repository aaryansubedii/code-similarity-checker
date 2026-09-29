import hashlib


def hash_token_sequence(tokens: list[str]) -> int:
    joined = " ".join(tokens)
    digest = hashlib.md5(joined.encode()).hexdigest()
    return int(digest[:8], 16)


def get_kgram_hashes(tokens_with_lines: list[tuple[str, int]], k: int = 5) -> list[tuple[int, int, int]]:
    """
    Splits (token, line) pairs into overlapping k-grams and hashes each one.
    Returns list of (hash, start_line, end_line) so matches can be traced
    to the actual source lines they span.
    """
    if len(tokens_with_lines) < k:
        tokens = [t for t, _ in tokens_with_lines]
        lines = [l for _, l in tokens_with_lines]
        h = hash_token_sequence(tokens)
        return [(h, lines[0] if lines else 0, lines[-1] if lines else 0)]

    hashes = []
    for i in range(len(tokens_with_lines) - k + 1):
        window = tokens_with_lines[i:i + k]
        tokens = [t for t, _ in window]
        lines = [l for _, l in window]
        h = hash_token_sequence(tokens)
        hashes.append((h, lines[0], lines[-1]))  # (hash, start_line, end_line)
    return hashes


def winnow(hashes: list[tuple[int, int, int]], window_size: int = 4) -> set[tuple[int, int, int]]:
    """
    Winnowing algorithm: keeps only the minimum hash in each sliding window
    of hashes (rightmost tie-break), while preserving line-range info.
    """
    if len(hashes) < window_size:
        return set(hashes)

    fingerprints = set()
    last_selected_start_line = -1

    for i in range(len(hashes) - window_size + 1):
        window = hashes[i:i + window_size]
        min_hash = min(h for h, _, _ in window)
        candidates = [(h, s, e) for h, s, e in window if h == min_hash]
        chosen = candidates[-1]

        if chosen[1] != last_selected_start_line:
            fingerprints.add(chosen)
            last_selected_start_line = chosen[1]

    return fingerprints


if __name__ == "__main__":
    from tokenizer import tokenize_with_lines

    sample1 = """
def calculate_total(price, quantity):
    total = price * quantity
    if total > 100:
        return total * 0.9
    return total
"""

    t1 = tokenize_with_lines(sample1)
    h1 = get_kgram_hashes(t1, k=5)
    f1 = winnow(h1, window_size=4)

    print("Fingerprints (hash, start_line, end_line):")
    for fp in sorted(f1, key=lambda x: x[1]):
        print(fp)