from typing import Tuple, List, Dict
import math


class JaroWinklerNGramSearch:

    def __init__(
        self,
        ngram_range: Tuple[int, int] = (1, 3),
        ngram_significance: float = 1.0,
        smooth_idf: bool = True,
    ) -> None:

        min_n, max_n = ngram_range

        if min_n <= 0:
            raise ValueError("The smallest n-gram is one.")

        if max_n < min_n:
            raise ValueError(
                "The largest n-gram cannot have a number "
                "of symbols smaller than min_ngram."
            )

        self.min_n = min_n
        self.max_n = max_n

        if ngram_significance < 1:
            raise ValueError("ngram_significance must be >= 1.")

        self.ngram_significance = ngram_significance

        self.smooth_idf = smooth_idf

        # ========================================================
        # Data
        # ========================================================

        self.words_: Tuple[str, ...] = ()

        self.Vocab: List[str] = []

        self.VocabIndex: Dict[str, int] = {}

        self.WordsData: List[Dict] = []

    # ============================================================
    # Extract ngrams
    # ============================================================

    def _extract_ngrams_and_index(
        self, word: str
    ) -> Dict[int, Dict[str, Tuple[int, ...]]]:
        """
        Բառից ստանում ենք n-gram-ները և
        դրանց բոլոր դիրքերը։
        """

        word_len = len(word)

        grams = {}

        for n in range(self.min_n, self.max_n + 1):

            if n > word_len:
                continue

            n_gram = {}

            for i in range(word_len - n + 1):

                gram = word[i : i + n]

                if gram in n_gram:
                    n_gram[gram] += (i,)
                else:
                    n_gram[gram] = (i,)

            grams[n] = n_gram

        return grams

    # ============================================================
    # Term Frequency
    # ============================================================

    def _term_freq(self, word: str) -> Dict[str, Tuple[Tuple[int, ...], float]]:

        n_grams_and_index = self._extract_ngrams_and_index(word)

        ngram_index = {}

        tf = {}

        total = 0

        for n in range(self.min_n, self.max_n + 1):

            grams_index = n_grams_and_index.get(n)

            if grams_index is None:
                continue

            ngram_index.update(grams_index)

            # ----------------------------------------------------
            # n-gram-ի նշանակության weight
            # ----------------------------------------------------

            weight = math.pow(math.sqrt(n), self.ngram_significance)

            for gram, indexes in grams_index.items():

                gram_count = len(indexes)

                total += gram_count

                tf[gram] = tf.get(gram, 0.0) + gram_count * weight

        # --------------------------------------------------------
        # Normalize TF
        # --------------------------------------------------------

        for gram in tf:

            tf[gram] /= total

        # --------------------------------------------------------
        # Միացնում ենք position + TF
        # --------------------------------------------------------

        return {gram: (ngram_index[gram], tf[gram]) for gram in tf}

    # ============================================================
    # Position score
    # ============================================================

    @staticmethod
    def _position_score(
        long_pos: Tuple[int, ...], short_pos: Tuple[int, ...], tfidf: float
    ) -> float:
        """
        Նույն greedy ալգորիթմը, ինչ C++-ում։

        long_pos  -> ավելի երկար position list
        short_pos -> ավելի կարճ position list
        """

        short_ind = 0
        long_ind = 0

        short_size = len(short_pos)
        long_size = len(long_pos)

        result = 0.0

        while short_ind < short_size:

            best_dif = abs(long_pos[long_ind] - short_pos[short_ind])

            if best_dif == 0:

                result += tfidf

                short_ind += 1
                long_ind += 1

                continue

            while long_ind < long_size - 1:

                current_dif = abs(short_pos[short_ind] - long_pos[long_ind + 1])

                if current_dif < best_dif:

                    best_dif = current_dif
                    long_ind += 1

                else:

                    break

            d = best_dif + 1.0

            result += tfidf / (d * d * d * d * d)

            long_ind += 1
            short_ind += 1

        return result

    # ============================================================
    # Fit
    # ============================================================

    def fit(self, words_data: List[str]) -> "JaroWinklerNGramSearch":

        # ========================================================
        # Store words
        # ========================================================

        self.words_ = tuple(words_data)

        count_words = len(words_data)

        # ========================================================
        # All documents TF data
        # ========================================================

        all_docs_tf_data = []

        # ========================================================
        # Document frequency
        # ========================================================

        count_words_with_in_ngram = {}

        # ========================================================
        # Calculate TF
        # ========================================================

        for word in words_data:

            ngram_indexes_TF = self._term_freq(word)

            all_docs_tf_data.append(ngram_indexes_TF)

            # ----------------------------------------------------
            # Յուրաքանչյուր ngram-ը այս document-ում
            # միայն մեկ անգամ ենք հաշվում
            # ----------------------------------------------------

            for gram in ngram_indexes_TF:

                count_words_with_in_ngram[gram] = (
                    count_words_with_in_ngram.get(gram, 0) + 1
                )

        # ========================================================
        # IDF
        # ========================================================

        if self.smooth_idf:

            idf_map = {
                gram: math.log((count_words + 1) / (count + 1)) + 1.0
                for gram, count in count_words_with_in_ngram.items()
            }

        else:

            idf_map = {
                gram: math.log(count_words / count)
                for gram, count in count_words_with_in_ngram.items()
            }

        # ========================================================
        # Sorted Vocab
        # ========================================================

        self.Vocab = sorted(count_words_with_in_ngram.keys(), key=lambda x: (len(x), x))

        # ========================================================
        # ngram -> index
        # ========================================================

        self.VocabIndex = {ngram: index for index, ngram in enumerate(self.Vocab)}

        # ========================================================
        # WordsData
        # ========================================================

        self.WordsData = []

        for i in range(count_words):

            NgPosTF = all_docs_tf_data[i]

            ngrams = []

            # ----------------------------------------------------
            # Միայն տվյալ բառի առկա ngram-ներով ենք անցնում
            #
            # ոչ թե ամբողջ Vocab-ով
            # ----------------------------------------------------

            for ngram, (positions, tf) in NgPosTF.items():

                index = self.VocabIndex[ngram]

                idf = idf_map[ngram]

                ngrams.append(
                    {"index": index, "tfidf": tf * idf, "positions": positions}
                )

            # ----------------------------------------------------
            # C++-ի նման sorted index
            # ----------------------------------------------------

            ngrams.sort(key=lambda x: x["index"])

            self.WordsData.append({"word": words_data[i], "ngrams": ngrams})

        return self

    # ============================================================
    # Query vectorization
    # ============================================================

    def _vectorize_query(self, query: str):

        tf_data = self._term_freq(query)

        result = []

        for gram, (positions, tf) in tf_data.items():

            index = self.VocabIndex.get(gram)

            if index is None:
                continue

            result.append({"index": index, "positions": positions})

        # --------------------------------------------------------
        # C++-ի նման sorted index
        # --------------------------------------------------------

        result.sort(key=lambda x: x["index"])

        return result

    # ============================================================
    # Search
    # ============================================================

    def search(self, query: str):

        query_vec = self._vectorize_query(query)

        top_result = []

        # ========================================================
        # Search բոլոր բառերի մեջ
        # ========================================================

        for word in self.WordsData:

            i = 0
            j = 0

            query_size = len(query_vec)

            word_ngrams = word["ngrams"]

            word_size = len(word_ngrams)

            score = 0.0

            # ====================================================
            # Two-pointer search
            # ====================================================

            while i < query_size and j < word_size:

                query_index = query_vec[i]["index"]

                word_index = word_ngrams[j]["index"]

                if query_index == word_index:

                    query_positions = query_vec[i]["positions"]

                    word_positions = word_ngrams[j]["positions"]

                    tfidf = word_ngrams[j]["tfidf"]

                    query_len = len(query_positions)

                    word_len = len(word_positions)

                    # --------------------------------------------
                    # Position list-երը նույն չափի են
                    # --------------------------------------------

                    if query_len == word_len:

                        for k in range(query_len):

                            pos_diff = abs(query_positions[k] - word_positions[k])

                            d = pos_diff + 1.0

                            score += tfidf / (d * d * d * d * d)

                    # --------------------------------------------
                    # Query-ն ավելի երկար է
                    # --------------------------------------------

                    elif query_len > word_len:

                        score += self._position_score(
                            query_positions, word_positions, tfidf
                        )

                    # --------------------------------------------
                    # Word-ն ավելի երկար է
                    # --------------------------------------------

                    else:

                        score += self._position_score(
                            word_positions, query_positions, tfidf
                        )

                    i += 1
                    j += 1

                elif query_index < word_index:

                    i += 1

                else:

                    j += 1

            # ====================================================
            # Top result
            # ====================================================

            top_result.append((word["word"], score))

        # ========================================================
        # Top-5
        # ========================================================

        top_result.sort(key=lambda x: x[1], reverse=True)

        return top_result[:5]
