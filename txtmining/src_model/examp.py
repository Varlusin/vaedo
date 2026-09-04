


def best_pos_difference(long_pos, short_pos):

    long_ind = 0
    short_ind = 0

    best_rez = []

    while short_ind < len(short_pos):

        best_dif = abs(
            short_pos[short_ind] -
            long_pos[long_ind]
        )

        # exact match
        if best_dif == 0:
            best_rez.append(0)

            short_ind += 1
            long_ind += 1

            continue

        best_long_ind = long_ind

        while long_ind < len(long_pos) - 1:

            next_long_ind = long_ind + 1

            current_dif = abs(
                short_pos[short_ind] -
                long_pos[next_long_ind]
            )

            if current_dif < best_dif:

                best_dif = current_dif
                best_long_ind = next_long_ind

                long_ind = next_long_ind

            else:
                # Քանի որ long_pos sorted է,
                # հաջորդները նույնպես այլևս չեն բարելավի
                # այս short position-ի արդյունքը։
                break

        best_rez.append(best_dif)

        # ընտրված long position-ը այլևս չի օգտագործվելու
        long_ind = best_long_ind + 1

        short_ind += 1

    return best_rez




if __name__ == "__main__":

    print(best_pos_difference([0, 4, 5, 7],[4] ))
    