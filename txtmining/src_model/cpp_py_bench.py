import time
import sys
import random
import string

sys.path.append("/home/vardan/Desktop/src_model/cpp")

import my_module
from transliterate import unicodelowersplit as uls
from py_ex import JaroWinklerNGramSearch as JWS


# ============================================================
# 1. Բազային բառերը
# ============================================================

stop_words = (    "c c. city town "    "ք ք․ քաղաք qaxaq "    "город гор гор. "    "village vlg vil v v. "    "գ գ․ գյուղ "    "համայնք "    "с с. село "    "п п. посёлок "    "д д. деревня "    "region province "    "մ մ․ մարզ "    "ավան "    "обл область край")

ln_code, stop_words = uls(stop_words)


# ============================================================
# 2. C++ model
# ============================================================

mod_cpp = my_module.JaroNGramSearch(min_N=1,max_N=5,N_signif = 2)

s = time.perf_counter()
mod_cpp.fit(stop_words)
e = time.perf_counter()

cpp_fit_time = e - s


# ============================================================
# 3. Python model
# ============================================================

mod_py = JWS((1, 5))

s = time.perf_counter()
mod_py.fit(stop_words)
e = time.perf_counter()

py_fit_time = e - s


print("=" * 70)
print("FIT PERFORMANCE")
print("=" * 70)
print(f"C++ fit : {cpp_fit_time * 1000:.3f} ms")
print(f"Python  : {py_fit_time * 1000:.3f} ms")


# ============================================================
# 4. Random test-data generator
# ============================================================

stop_words = (
    " city town "
    " քաղաք qaxaq "
    "город гор гор. "
    "village vlg vil"
    " գյուղ "
    "համայնք "
    " село "
    " посёлок "
    " деревня "
    "region province "
    " մարզ "
    "ավան "
    "обл область край"
)

ln_code, stop_words = uls(stop_words)




ALPHABET = string.ascii_lowercase + "./"


def mutate_word(word, changes):

    chars = list(word)

    for _ in range(changes):

        operation = random.choice(
            ["replace", "insert"]
        )

        if not chars:
            chars.append(
                random.choice(ALPHABET)
            )
            continue

        if operation == "replace":

            pos = random.randrange(
                len(chars)
            )

            chars[pos] = random.choice(
                ALPHABET
            )

        else:

            pos = random.randrange(
                len(chars) + 1
            )

            chars.insert(
                pos,
                random.choice(ALPHABET)
            )

    return "".join(chars)


def generate_test_data(
    words,
    variants_min=10,
    variants_max=15
):

    result = {}

    for word in words:

        count = random.randint(
            variants_min,
            variants_max
        )

        variants = set()

        while len(variants) < count:

            if len(word) == 1:
                changes = 1
            else:
                changes = random.randint(1, 3)

            variant = mutate_word(
                word,
                changes
            )

            if variant != word:
                variants.add(variant)

        result[word] = list(variants)

    return result


# ============================================================
# 5. Generate test data
# ============================================================

test_data = generate_test_data(
    stop_words,
    variants_min=10,
    variants_max=15
)


# ============================================================
# 6. Prepare queries
# ============================================================

test_queries = []

for original, variants in test_data.items():

    for variant in variants:

        test_queries.append(
            (original, variant)
        )


print()
print("=" * 70)
print("TEST DATA")
print("=" * 70)

print(
    f"Original words : {len(test_data)}"
)

print(
    f"Test queries   : {len(test_queries)}"
)


# ============================================================
# 7. Search test
# ============================================================

times = []

found_count = 0


print()
print("=" * 70)
print("C++ SEARCH TEST")
print("=" * 70)


for i, (original, q) in enumerate(
    test_queries,
    1
):

    s = time.perf_counter()

    result = mod_cpp.search(q)

    e = time.perf_counter()

    elapsed = e - s

    times.append(elapsed)


    # --------------------------------------------------------
    # Ստուգում ենք՝ original բառը Top-5-ում կա՞
    # --------------------------------------------------------

    found = any(
        word == original
        for word, score in result
    )

    if found:
        found_count += 1


    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print(
        f"[{i:04}] "
        f"query={q!r:<15} "
        f"original={original!r:<15} "
        f"time={elapsed * 1000:>8.3f} ms "
        f"found={'YES' if found else 'NO'}"
    )

    for rank, (word, score) in enumerate(
        result,
        1
    ):

        print(
            f"       {rank}. "
            f"{word:<25} "
            f"score={score:.6f}"
        )


# ============================================================
# 8. Statistics
# ============================================================

total_queries = len(test_queries)

total_time = sum(times)

average_time = (
    total_time / total_queries
    if total_queries
    else 0
)

min_time = (
    min(times)
    if times
    else 0
)

max_time = (
    max(times)
    if times
    else 0
)

accuracy = (
    found_count / total_queries * 100
    if total_queries
    else 0
)


# ============================================================
# 9. Final result
# ============================================================

print()
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)

print(
    f"Total queries : {total_queries}"
)

print(
    f"Found Top-5   : {found_count}"
)

print(
    f"Accuracy      : {accuracy:.2f}%"
)

print(
    f"Total time    : {total_time * 1000:.3f} ms"
)

print(
    f"Average time  : {average_time * 1000:.3f} ms"
)

print(
    f"Min time      : {min_time * 1000:.3f} ms"
)

print(
    f"Max time      : {max_time * 1000:.3f} ms"
)

print("=" * 70)




s= time.time()

a = mod_cpp.search('pasiolok')
e = time.time()

cpp_t = e-s

print(a)



s= time.time()

a = mod_py.search('pasiolok')
e = time.time()

print(a)


py_t = e-s

print(cpp_t, py_t)