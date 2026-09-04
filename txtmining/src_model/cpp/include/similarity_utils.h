#pragma once

#include <string>
#include <vector>
#include <unordered_map>

struct QueryNgramData
{
    int index;
    std::vector<int> positions;
};

using QueryData =
    std::vector<QueryNgramData>;

QueryData vectorize_query(
    const std::string &query,
    int min_N,
    int max_N,
    const std::unordered_map<
        int,
        std::unordered_map<std::string, int>> &vocab_index);

// ===================================================================================

double position_score(
    const std::vector<int>& long_pos,
    const std::vector<int>& short_pos,
    int long_size,
    int short_size,
    double tfidf);

// ===============================================================================

// ------------------------------------------------------------
// Top 5
// ------------------------------------------------------------
// Նոր արդյունքը տեղադրում է top_result-ի ճիշտ դիրքում։
//
// top_result -> միշտ պահում է առավելագույնը 5 արդյունք
// top_size   -> տվյալ պահին քանի իրական արդյունք կա
void insert_top5(
    std::array<std::pair<std::string, double>, 5>& top_result,
    size_t& top_size,
    const std::string& word,
    double score);
