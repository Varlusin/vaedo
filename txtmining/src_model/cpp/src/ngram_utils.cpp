#include <ngram_utils.h>

#include <cmath>
#include <utility>
#include <algorithm>

NGramIndex extract_ngrams_and_index(
    const std::string &word,
    int min_n,
    int max_n)
{
    NGramIndex grams;

    int word_len = word.length();

    for (int n = min_n; n <= max_n; ++n)
    {
        if (n > word_len)
            continue;

        N_gram n_gram;

        for (int i = 0; i <= word_len - n; ++i)
        {
            std::string gram = word.substr(i, n);

            n_gram[gram].push_back(i);
        }

        grams[n] = std::move(n_gram);
    }

    return grams;
}

TFResult term_freq(
    const std::string &word,
    int min_n,
    int max_n,
    double ngram_significance)
{
    auto n_grams_and_index =
        extract_ngrams_and_index(
            word,
            min_n,
            max_n);

    N_gram ngram_index;

    int total = 0;

    Tf tf;

    for (int n = min_n; n <= max_n; ++n)
    {
        auto grams_it =
            n_grams_and_index.find(n);

        if (grams_it == n_grams_and_index.end())
            continue;

        const auto &grams_index =
            grams_it->second;

        for (const auto &[gram, indexes] : grams_index)
        {
            ngram_index[gram] = indexes;
        }
        // weigth սա ամեն n֊ին համապատասխան կշիռն է այսինքն որքան մեծ է n ը այնքան մեծ է   weigth
        double weight =
            std::pow(
                std::sqrt(static_cast<double>(n)),
                ngram_significance);

        for (const auto &[gram, indexes] : grams_index)
        {
            int gram_count = indexes.size();

            total += gram_count;

            tf[gram] += gram_count * weight;
        }
    }

    TFResult result;

    for (const auto &[gram, value] : tf)
    {
        double final_tf =
            value / total;

        result[gram] = {
            ngram_index[gram],
            final_tf};
    }

    return result;
}

std::vector<std::string> sortind_create_vocab_vec(
    const std::unordered_map<std::string, int> &all_gram_and_freq)

{
    std::vector<
        std::string>
        vocab;

    for (const auto &[ngram, freq] : all_gram_and_freq)
    {
        vocab.push_back(ngram);
    }

    std::sort(
        vocab.begin(),
        vocab.end(),
        [](const std::string &a, const std::string &b)
        {
            if (a.length() != b.length())
                return a.length() < b.length();

            return a < b;
        });
    return vocab;
}

std::unordered_map<
    int,
    std::unordered_map<std::string, int>>
create_vocabIndec_map(
    const std::vector<std::string> &vocab)
{
    std::unordered_map<
        int,
        std::unordered_map<std::string, int>>
        VocabIndex;

    for (size_t i = 0; i < vocab.size(); ++i)
    {
        int N = vocab[i].size();

        VocabIndex[N].emplace(
            vocab[i],
            static_cast<int>(i));
    }

    return VocabIndex;
}

std::vector<FinalFitWordData> normalization_tfidf(
    std::vector<WordData> &WordsData)
{
    std::vector<FinalFitWordData> FinalWordsData;
    FinalWordsData.reserve(WordsData.size());

    for (size_t i = 0; i < WordsData.size(); ++i)
    {
        double score = 0.0;

        WordData &worddata = WordsData[i];

        // Հաշվում ենք տվյալ բառի բոլոր n-gram-ների ընդհանուր TF-IDF score-ը
        for (const auto &ngram_data_each_word : worddata.ngrams)
        {
            score +=
                ngram_data_each_word.tfidf *
                ngram_data_each_word.positions.size();
        }

        // Նորմալիզացնում ենք յուրաքանչյուր n-gram-ի TF-IDF-ը
        if (score > 0.0)
        {
            for (auto &ngram_data_each_word : worddata.ngrams)
            {
                ngram_data_each_word.tfidf /= score;
            }
        }

        // Միայն այստեղ ենք ստեղծում final տվյալը
        FinalFitWordData final_data;

        final_data.word = worddata.word;

        // Այստեղ պահում ենք բառի երկարությունը
        final_data.count_term =
            static_cast<int>(worddata.word.size());

        final_data.ngrams = worddata.ngrams;

        FinalWordsData.push_back(final_data);
    }

    return FinalWordsData;
}