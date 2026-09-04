#include <similarity_utils.h>
#include <algorithm>
#include <vector>
#include <limits>
#include <cmath>




QueryData vectorize_query(

    const std::string &query,
    int min_N,
    int max_N,
    const std::unordered_map<
        int,
        std::unordered_map<std::string, int>> &vocab_index)
{
    QueryData query_data;

    int query_len = query.length();

    for (int n = min_N; n <= max_N; ++n)
    {
        if (n > query_len)
            continue;

        const auto &vocab_n =
            vocab_index.at(n);

        std::unordered_map<
            std::string,
            std::vector<int>>
            n_gram;

        for (int i = 0; i <= query_len - n; ++i)
        {
            std::string gram =
                query.substr(i, n);

            n_gram[gram].push_back(i);
        }

        for (const auto &[gram, positions] : n_gram)
        {
            auto it =
                vocab_n.find(gram);

            if (it != vocab_n.end())
            {
                QueryNgramData data;

                data.index = it->second;
                data.positions = positions;

                query_data.push_back(data);
            }
        }
    }

    std::sort(
        query_data.begin(),
        query_data.end(),
        [](const QueryNgramData &a,
           const QueryNgramData &b)
        {
            return a.index < b.index;
        });

    return query_data;
}

// ============================================================
// Find the best position matching
// ============================================================
//
// Q և W vector-ները ՊԱՐՏԱԴԻՐ sorted են:
//
// Օրինակ:
//
// Q = [2, 7, 12, 18, 20]
// W = [1, 8, 19]
//
// Q-ն ունի 5 position, W-ն՝ 3:
//
// Այսինքն Q-ից պետք է skip անել ճիշտ 2 position:
//
//     Q:  q0  q1  q2  q3  q4
//              X       X
//     W:  w0      w1      w2
//
// Բայց մենք նախապես չգիտենք, թե որ Q-երն են պետք skip անել:
//
// Ֆունկցիան գտնում է այն order-preserving matching-ը,
// որի position difference-ների գումարը նվազագույնն է:
//
// Օրինակ հնարավոր է:
//
//     q0 -> w0
//     q2 -> w1
//     q4 -> w2
//
// կամ:
//
//     q1 -> w0
//     q2 -> w1
//     q3 -> w2
//
// և այլն:
//
// Քանի որ positions-ը sorted են, matching-ի հերթականությունը
// երբեք չի փոխվում:
//
// q_i -> w_j
//
// կատարելուց հետո հաջորդ query position-ը չի կարող գնալ
// w_j-ից առաջ գտնվող word position-ի հետ:
//
// ============================================================

double position_score(
    const std::vector<int> &long_pos,
    const std::vector<int> &short_pos,
    int long_size,
    int short_size,
    double tfidf)
{
    int short_ind = 0;
    int long_ind = 0;

    double result = 0.0;

    while (short_ind < short_size)
    {
        int best_dif = std::abs(
            long_pos[long_ind] - short_pos[short_ind]);

        if (best_dif == 0)
        {
            ++short_ind;
            ++long_ind;
            continue;
        }

        while (long_ind < long_size - 1)
        {
            int current_dif = std::abs(
                short_pos[short_ind] -
                long_pos[long_ind + 1]);

            if (current_dif < best_dif)
            {
                best_dif = current_dif;
                ++long_ind;
            }
            else
            {
                break;
            }
        }

        double d = best_dif + 1.0;
        result += tfidf / (d * d);

        ++long_ind;
        ++short_ind;
    }

    return result;
}


//============================================================================================

// ============================================================
// Top 5
// ============================================================

void insert_top5(
    std::array<std::pair<std::string, double>, 5>& top_result,
    size_t& top_size,
    const std::string& word,
    double score)
{
    // Եթե արդեն ունենք 5 արդյունք,
    // և նոր score-ը 5-րդից լավը չէ,
    // ապա ոչինչ չենք անում։
    if (top_size == 5 &&
        score <= top_result[4].second)
    {
        return;
    }

    // Գտնում ենք նոր score-ի ճիշտ դիրքը։
    //
    // top_result-ը դասավորված է մեծից փոքր։
    size_t pos = 0;

    while (
        pos < top_size &&
        top_result[pos].second >= score)
    {
        ++pos;
    }

    // Առավելագույնը 4 element կարող է պետք լինել տեղափոխել։
    size_t end = std::min(top_size, size_t(4));

    // Ավելի փոքր score-երը տեղափոխում ենք աջ։
    for (size_t i = end; i > pos; --i)
    {
        top_result[i] =
            std::move(top_result[i - 1]);
    }

    // Նոր արդյունքը դնում ենք ճիշտ դիրքում։
    top_result[pos] = {word, score};

    // Եթե դեռ 5 արդյունք չունեինք,
    // մեծացնում ենք իրական element-ների քանակը։
    if (top_size < 5)
    {
        ++top_size;
    }
}