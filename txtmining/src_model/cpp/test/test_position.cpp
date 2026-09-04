#include <iostream>
#include <vector>

#include <similarity_utils.h>


int main()
{
    // --------------------------------------------------------
    // Query positions
    // --------------------------------------------------------
    //
    // 5 position
    //
    std::vector<int> query_positions =
    {
        0, 1, 10, 15, 20
    };


    // --------------------------------------------------------
    // Word positions
    // --------------------------------------------------------
    //
    // 3 position
    //
    // Query-ից պետք է անտեսվի ճիշտ 2 position։
    //
    std::vector<int> word_positions =
    {
        1, 2,14, 21
    };


    // --------------------------------------------------------
    // Find best matching
    // --------------------------------------------------------

    PositionMatch result =
        find_best_position_match(
            query_positions,
            word_positions);


    // --------------------------------------------------------
    // Print total difference
    // --------------------------------------------------------

    std::cout
        << "Total difference: "
        << result.total_difference
        << "\n";


    // --------------------------------------------------------
    // Print selected pairs
    // --------------------------------------------------------

    std::cout
        << "Pairs:\n";


    for (const auto& [q_pos, w_pos] :
         result.pairs)
    {
        std::cout
            << "Q[" << q_pos << "]"
            << " -> "
            << "W[" << w_pos << "]"
            << " | diff = "
            << std::abs(q_pos - w_pos)
            << "\n";
    }


    return 0;
}