#include <JaroNGramSearch.h>
#include <ngram_utils.h>
#include <similarity_utils.h>
#include <cmath>

// ============================================================
// Constructor
// ============================================================

JaroNGramSearch::JaroNGramSearch(
    int min_N,
    int max_N,
    double N_signif)
    : min_N(min_N),
      max_N(max_N),
      N_signif(N_signif)
{
}

// ============================================================
// fit()
// ============================================================

void JaroNGramSearch::fit(
    const std::vector<std::string> &input_words)
{
    std::vector<TFResult> all_docs_tf_data;

    std::unordered_map<std::string, int>
        ngram_document_frequency;

    std::unordered_map<std::string, double>
        idf_map;

    size_t count_worlds = input_words.size();

    std::vector<WordData> WordsData;

    // ========================================================
    // Calculate TF and document frequency
    // ========================================================

    for (const auto &word : input_words)
    {
        TFResult NgIndTF =
            term_freq(
                word,
                min_N,
                max_N,
                N_signif);

        all_docs_tf_data.push_back(NgIndTF);

        for (const auto &item : NgIndTF)
        {
            ngram_document_frequency[item.first] += 1;
        }
    }

    // ========================================================
    // Calculate IDF
    // ========================================================

    for (const auto &[ngram, freq] :
         ngram_document_frequency)
    {
        idf_map[ngram] =
            std::log(
                static_cast<double>(count_worlds) / freq) +
            1.0;
    }

    // ========================================================
    // Create ngram -> index
    // ========================================================


    std::vector<std::string> Vocab;
    
    Vocab = sortind_create_vocab_vec(ngram_document_frequency);

    VocabIndex =
        create_vocabIndec_map(
            Vocab);

    // ========================================================
    // Create FinalWordsData
    // ========================================================
    for (size_t i = 0; i < count_worlds; ++i)
    {
        TFResult NgPosTF =
            all_docs_tf_data[i];

        WordData word_data;

        word_data.word =
            input_words[i];

        for (size_t index = 0; index < Vocab.size(); ++index)
        {
            const std::string &ngram =
                Vocab[index];

            auto it =
                NgPosTF.find(ngram);

            if (it != NgPosTF.end())
            {
                const auto &positions =
                    it->second.first;

                double tf =
                    it->second.second;

                double idf =
                    idf_map[ngram];

                NgramData data{
                    static_cast<int>(index),
                    tf * idf,
                    positions};

                word_data.ngrams.push_back(data);
            }
        }

        WordsData.push_back(word_data);
        FinalWordsData = normalization_tfidf(WordsData);
    }
}

// ============================================================
// search()
// ============================================================

std::array<std::pair<std::string, double>, 5>
JaroNGramSearch::search(
    const std::string &query)
{
    QueryData query_vec = vectorize_query(
        query,
        min_N,
        max_N,
        VocabIndex);

    // Այստեղ պահելու ենք միայն լավագույն 5 արդյունքները։
    std::array<std::pair<std::string, double>, 5> top_result;

    // Քանի իրական արդյունք ունենք։
    size_t top_size = 0;

    for (const auto &word : FinalWordsData)
    {
        size_t i = 0;
        size_t j = 0;

        double score = 0.0;

        // Query-ի և word-ի n-gram-երը
        // արդեն sorted են ըստ index-ի։
        //
        // Դրա շնորհիվ օգտագործում ենք երկու pointer։
        while (
            i < query_vec.size() &&
            j < word.ngrams.size())
        {
            if (query_vec[i].index ==
                word.ngrams[j].index)
            {
                // ------------------------------------------------
                // MATCH
                // ------------------------------------------------

                const std::vector<int> &query_positions =
                    query_vec[i].positions;

                const std::vector<int> &word_positions =
                    word.ngrams[j].positions;

                const double tfidf =
                    word.ngrams[j].tfidf;

                size_t query_size =
                    query_positions.size();

                size_t word_size =
                    word_positions.size();

                // ------------------------------------------------
                // Նույն քանակի position-ներ
                // ------------------------------------------------

                if (query_size == word_size)
                {
                    for (size_t k = 0;
                         k < query_size;
                         ++k)
                    {
                        int pos_diff =
                            std::abs(
                                query_positions[k] -
                                word_positions[k]);

                        double d =
                            pos_diff + 1.0;

                        score +=
                            tfidf /
                            (d * d);
                    }
                }

                // ------------------------------------------------
                // Query-ն ավելի շատ position ունի
                // ------------------------------------------------

                else if (query_size > word_size)
                {
                    score += position_score(
                        query_positions,
                        word_positions,
                        query_size,
                        word_size,
                        tfidf);
                }

                // ------------------------------------------------
                // Word-ն ավելի շատ position ունի
                // ------------------------------------------------

                else
                {
                    score += position_score(
                        word_positions,
                        query_positions,
                        word_size,
                        query_size,
                        tfidf);
                }

                ++i;
                ++j;
            }

            // Query-ի index-ը փոքր է։
            // Word-ի այս n-gram-ը չենք գտել,
            // հետևաբար առաջ ենք տանում query pointer-ը։
            else if (
                query_vec[i].index <
                word.ngrams[j].index)
            {
                ++i;
            }

            // Word-ի index-ը փոքր է։
            // Առաջ ենք տանում word pointer-ը։
            else
            {
                ++j;
            }
        }

        // --------------------------------------------------------
        // Այս word-ի score-ը պատրաստ է։
        //
        // Պահում ենք միայն Top-5-ը։
        // --------------------------------------------------------

        insert_top5(
            top_result,
            top_size,
            word.word,
            score);
    }

    return top_result;
}
