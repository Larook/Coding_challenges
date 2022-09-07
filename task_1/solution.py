"""

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?")
Output:
    did you see last night's episode?

Input:
solution.solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!")
Output:
    Yeah! I can't believe Lance lost his job at the colony!!

"""


def solution(input: str) -> str:
    fwd_order_l_min = ord('a')
    fwd_order_l_max = ord('z')
    middle_index_l = fwd_order_l_min + int((fwd_order_l_max - fwd_order_l_min) / 2) + (
                fwd_order_l_max - fwd_order_l_min) % 2

    # fwd_order_u_min = ord('A')
    # fwd_order_u_max = ord('Z')
    # middle_index_u = fwd_order_u_min + int((fwd_order_u_max - fwd_order_u_min) / 2) + (
    #             fwd_order_u_max - fwd_order_u_min) % 2

    output_chars = []

    for sign_ in input:
        if ord(sign_) in range(fwd_order_l_min, fwd_order_l_max + 1):
            # it's an lowercase letter
            # when lower or higher than the middle - doesnt matter
            delta = middle_index_l - ord(sign_)
            out_id = ord(sign_) + 2*delta - 1
            # sign_out = chr(out_id)
            output_chars.append(chr(out_id))

        # elif ord(sign_) in range(fwd_order_u_min, fwd_order_u_max + 1):
        #     # it's an uppercase letter
        #     delta = middle_index_u - ord(sign_)
        #     out_id = ord(sign_) + 2*delta - 1
        #     output_chars.append(chr(out_id))

        else:
            # it's a special character or uppercase
            output_chars.append(sign_)

    output_string = ''.join(output_chars)

    return output_string


if __name__ == "__main__":
    test_in_1 = "wrw blf hvv ozhg mrtsg'h vkrhlwv?"
    test_out_1 = "did you see last night's episode?"
    test_txt_2 = "Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"
    test_out_2 = "Yeah! I can't believe Lance lost his job at the colony!!"


    out_1 = solution(test_in_1)
    print(out_1)

    out_2 = solution(test_txt_2)
    print(out_2)