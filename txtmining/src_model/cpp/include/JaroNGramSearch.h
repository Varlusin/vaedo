#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <utility>

struct NgramData
{
    int index;
    double tfidf;
    std::vector<int> positions;
};

struct WordData
{
    std::string word;
    std::vector<NgramData> ngrams;
};


struct FinalFitWordData
{
    std::string word;
    int count_term;
    std::vector<NgramData> ngrams;
};

class JaroNGramSearch
{
public:
    int min_N;
    int max_N;
    double N_signif;

    std::unordered_map<int, std::unordered_map<std::string, int>> VocabIndex;

    std::vector<FinalFitWordData> FinalWordsData;

    JaroNGramSearch(
        int min_N = 1,
        int max_N = 3,
        double N_signif = 1);

    void fit(
        const std::vector<std::string> &input_words);

    std::array<std::pair<std::string, double>, 5>
    search(
        const std::string &query);
};