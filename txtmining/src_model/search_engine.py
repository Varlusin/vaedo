from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

#  @dataclass add method __init__,  __repr__, __eq__ , methods automaticly.
from dataclasses import dataclass, field



from transliterate import unicodelowersplit as uls

import math
import numpy as np
from scipy import sparse


import pickle



def _extract_ngrams(text: str, ngram_range: Tuple[int, int]) -> List[str]:
    """

    """
    min_n, max_n = ngram_range
    text_len = len(text)
    grams = []
    for n in range(min_n, min(max_n, text_len) + 1):
        for i in range(text_len - n + 1):
            grams.append(text[i : i + n])
    return grams

def _term_freq(grams: Sequence[str]) -> Dict[str, float]:
    """
    """
    if not grams:
        return {}
    tf: Dict[str, int] = {}
    for g in grams:
        tf[g] = tf.get(g, 0) + 1
    total = len(grams)
    return {g: c / total for g, c in tf.items()}


@dataclass
class SearchIndex:
    """
    """
    ngram_range: Tuple[int, int] = (1, 4) # defoult
    smooth_idf: bool = True 
    # how many of the query's rarest n-grams to use for candidate generation
    candidate_grams: int = 6
    # skip building postings for n-grams that appear in more than this
    # fraction of documents -- they're useless for narrowing candidates and
    # only bloat the index
    max_df_ratio: float = 0.4
    vocabulary_: Dict[str, int] = field(default_factory=dict)
    idf_: np.ndarray = field(default_factory=lambda: np.zeros(0))
    matrix_: Optional[sparse.csr_matrix] = None  # (n_docs, n_grams), L2-normalized
    matrix_csc_: Optional[sparse.csc_matrix] = None  # for fast column (postings) access
    ids_: List = field(default_factory=list)  # external ids (e.g. DB primary keys)
    labels_: List[str] = field(default_factory=list)  # original strings, for display

    def fit(self, labels: Iterable[str], ids: Optional[Iterable] = None) -> "SearchIndex":
        """
        """
        # The clas holds a list of words from which it must make a fit and 
        # must say how similar the new word is to the given word.
        self.labels_ = list(labels)
        # all term frecuency list evri value dict into ngram : tf_value 
        doc_tfs: List[Dict[str, float]] = []
        
        n_docs = len(self.labels_) 

        df: Dict[str, int] = {}
        #  
        # go every word
        for label in self.labels_:
            # get an ngram list for the word
            grams = _extract_ngrams(label, self.ngram_range)
            # For the word we get the term frequency Dict of the ngram.
            tf = _term_freq(grams)
            # add the resulting tf dict for the word to all tfs
            doc_tfs.append(tf)
            for g in tf:
                df[g] = df.get(g, 0) + 1
        features = sorted(df.keys())
        self.vocabulary_ = {g: i for i, g in enumerate(features)}
        self.idf_ = np.zeros(len(features), dtype=np.float32)
        for g, col in self.vocabulary_.items():
            dfi = df[g]
            if self.smooth_idf:
                self.idf_[col] = math.log((n_docs + 1) / (dfi + 1)) + 1
            else:
                self.idf_[col] = math.log(n_docs / dfi) + 1

        rows, cols, data = [], [], []
        for r, tf in enumerate(doc_tfs):
            for g, tf_val in tf.items():
                col = self.vocabulary_[g]
                rows.append(r)
                cols.append(col)
                data.append(tf_val * self.idf_[col])
        
        m = sparse.csr_matrix(
            (data, (rows, cols)), shape=(n_docs, len(features)), dtype=np.float32
        )
        # L2-normalize rows so dot product == cosine similarity
        norms = np.sqrt(m.multiply(m).sum(axis=1)).A.ravel()
        norms[norms == 0] = 1.0
        m = sparse.diags(1.0 / norms) @ m
        self.matrix_ = m.tocsr()
        self.matrix_csc_ = m.tocsc()

        # mark n-grams too common to be useful for candidate pruning
        doc_freq = np.asarray((self.matrix_ != 0).sum(axis=0)).ravel()
        self._prunable = doc_freq <= (self.max_df_ratio * n_docs)

        return self



    def _vectorize_query(self, text: str) -> Dict[int, float]:
        grams = _extract_ngrams(text, self.ngram_range)
        tf = _term_freq(grams)
        vec: Dict[int, float] = {}
        for g, tf_val in tf.items():
            col = self.vocabulary_.get(g)
            if col is not None:
                vec[col] = tf_val * self.idf_[col]
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            vec = {c: v / norm for c, v in vec.items()}
        return vec

    def _candidate_docs(self, query_vec: Dict[int, float]) -> np.ndarray:
        # use the rarest (highest idf) grams that are still allowed to
        # narrow candidates, so one very common n-gram in the query can't
        # force us back to a full scan
        cols = [c for c in query_vec if self._prunable[c]] or list(query_vec)
        cols.sort(key=lambda c: -self.idf_[c])
        cols = cols[: self.candidate_grams]

        if not cols:
            # degenerate query (all grams too common / unseen vocab) --
            # fall back to scoring everything
            return np.arange(self.matrix_.shape[0])

        candidate_sets = [
            self.matrix_csc_.indices[
                self.matrix_csc_.indptr[c] : self.matrix_csc_.indptr[c + 1]
            ]
            for c in cols
        ]
        return np.unique(np.concatenate(candidate_sets))

    def search(
        self,
        query: str,
        top_k: int = 10,
        restrict_to: Optional[np.ndarray] = None,
    ) -> List[Tuple[object, str, float]]:
        """Return up to top_k (id, label, score) tuples, best first.

        restrict_to: optional array of row indices (into this index) to
        limit the search to -- e.g. only the streets belonging to a city
        that was already resolved from an earlier part of the query.
        """
        query_vec = self._vectorize_query(query)
        if not query_vec:
            return []

        candidates = self._candidate_docs(query_vec)
        if restrict_to is not None:
            candidates = np.intersect1d(candidates, restrict_to, assume_unique=False)
        if candidates.size == 0:
            return []

        q_cols = np.fromiter(query_vec.keys(), dtype=np.int64)
        q_vals = np.fromiter(query_vec.values(), dtype=np.float32)
        q_sparse = sparse.csr_matrix(
            (q_vals, (np.zeros_like(q_cols), q_cols)),
            shape=(1, self.matrix_.shape[1]),
        )

        sub = self.matrix_[candidates]
        scores = (sub @ q_sparse.T).toarray().ravel()

        nonzero = scores > 0
        if not np.any(nonzero):
            return []
        candidates = candidates[nonzero]
        scores = scores[nonzero]

        k = min(top_k, scores.size)
        # partial selection is O(n) instead of a full O(n log n) sort
        top_idx = np.argpartition(-scores, k - 1)[:k]
        top_idx = top_idx[np.argsort(-scores[top_idx])]

        return [
            (self.ids_[candidates[i]], self.labels_[candidates[i]], float(scores[i]))
            for i in top_idx
        ]

if __name__ == "__main__":
    stop_words = "c c.  city town  ք ք․ քաղաք qaxaq  город гор гор.  village, vlg, vil v v.  գ գ․  գյուղ համայնք с с. село п п. посёлок д д. деревня  region province մ մ․ մարզ  ավան обл, область, край"
    _, data =  uls(stop_words)
    a = SearchIndex()


    a.fit(data)
    print(a.search('town'))
