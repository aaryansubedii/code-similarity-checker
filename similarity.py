from tokenizer import tokenize_with_lines
from fingerprint import get_kgram_hashes, winnow


def compute_similarity(code1: str, code2: str, k: int = 5, window_size: int = 4) -> dict:
    """
    Compares two source files and returns a similarity score plus
    the actual matching line ranges in each file.
    """
    tokens1 = tokenize_with_lines(code1)
    tokens2 = tokenize_with_lines(code2)

    hashes1 = get_kgram_hashes(tokens1, k=k)
    hashes2 = get_kgram_hashes(tokens2, k=k)

    fp1 = winnow(hashes1, window_size=window_size)
    fp2 = winnow(hashes2, window_size=window_size)

    hash_set1 = {h for h, _, _ in fp1}
    hash_set2 = {h for h, _, _ in fp2}
    shared = hash_set1 & hash_set2

    union = hash_set1 | hash_set2
    similarity_score = len(shared) / len(union) if union else 0.0

    # Collect the actual line numbers involved in a shared fingerprint, per file
    matched_lines_1 = sorted({line for h, s, e in fp1 if h in shared for line in range(s, e + 1)})
    matched_lines_2 = sorted({line for h, s, e in fp2 if h in shared for line in range(s, e + 1)})

    return {
        "similarity_percent": round(similarity_score * 100, 1),
        "shared_fingerprints": len(shared),
        "total_fingerprints_1": len(fp1),
        "total_fingerprints_2": len(fp2),
        "matched_lines_1": matched_lines_1,
        "matched_lines_2": matched_lines_2,
    }


if __name__ == "__main__":
    sample1 = """
def calculate_total(price, quantity):
    total = price * quantity
    if total > 100:
        return total * 0.9
    return total
"""

    sample2 = """
def get_sum(x, y):
    result = x * y
    if result > 100:
        return result * 0.9
    return result
"""

    unrelated = """
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Some generic sound")
"""

    print("Renamed-variable comparison:")
    print(compute_similarity(sample1, sample2))

    print("\nUnrelated code comparison:")
    print(compute_similarity(sample1, unrelated))