#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <utility>
#include <JaroNGramSearch.h>

using N_gram =
    std::unordered_map<
        std::string,
        std::vector<int>>;

using NGramIndex =
    std::unordered_map<
        int,
        N_gram>;



using TFResult =
    std::unordered_map<
        std::string,
        std::pair<
            std::vector<int>,
            double>>;

using Tf =
    std::unordered_map<
        std::string,
        double>;

using SortedNgramIndex =
    std::vector<
        std::string>;



NGramIndex extract_ngrams_and_index(
    const std::string &word,
    int min_n,
    int max_n);

std::vector<FinalFitWordData> normalization_tfidf (
    std::vector<WordData> &WordsData
);








TFResult term_freq(
    const std::string &word,
    int min_n,
    int max_n,
    double ngram_significance);

std::vector<std::string> sortind_create_vocab_vec(
    const std::unordered_map<std::string, int> &all_gram_and_freq);

std::unordered_map<int, std::unordered_map<std::string, int>> create_vocabIndec_map(
    const std::vector<std::string> &vocab

);
