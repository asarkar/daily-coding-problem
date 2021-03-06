import pytest

from dp import functions as func


class TestDP:
    def test_num_decodings(self):
        assert func.num_decodings("226") == 3
        assert func.num_decodings("12") == 2
        assert func.num_decodings("111") == 3
        assert func.num_decodings("0") == 0
        assert func.num_decodings("01") == 0
        assert func.num_decodings("10") == 1
        assert func.num_decodings("101") == 1
        assert func.num_decodings("100") == 0
        assert func.num_decodings("110") == 1
        assert func.num_decodings("001") == 0
        assert func.num_decodings(
            "4757562545844617494555774581341211511296816786586787755257741178599337186486723247528324612117156948"
        ) == 589824

    def test_perfect_sq(self):
        assert func.perfect_sq(12) == 3
        assert func.perfect_sq(13) == 2
        assert func.perfect_sq(27) == 3

    def test_num_ways(self):
        matrix = [
            [0, 0, 1],
            [0, 0, 1],
            [1, 0, 0]
        ]
        assert func.num_ways(matrix) == 2

        matrix = [
            [0, 0, 0],
            [0, 0, 0]
        ]
        assert func.num_ways(matrix) == 3

    @pytest.mark.parametrize("nums, subset_sum", [
        ([1, 5, 11, 5], 11),
        ([1, 2, 3, 5], None),
        ([1, 2, 3, 4], 5),
        ([1, 1, 3, 4, 7], 8),
        ([2, 3, 4, 6], None),
        ([1, 2, 5], None),
        ([16, 14, 13, 13, 12, 10, 9, 3], 45),
        ([0, 1, 5, 6], 6)
    ])
    def test_equal_subset_sum(self, nums, subset_sum):
        subset = func.equal_subset_sum(nums)
        if subset_sum:
            assert sum(map(lambda i: nums[i], subset)) == subset_sum
        else:
            assert not subset

    @pytest.mark.parametrize("nums, diff", [
        ([5, 10, 15, 20, 25], 5),
        ([0, 1, 5, 6], 0),
        ([16, 14, 13, 13, 12, 10, 9, 3], 0)
    ])
    def test_min_subset_sum(self, nums, diff):
        x = sum(nums)
        subset = map(lambda i: nums[i], func.min_subset_sum(nums))
        y = sum(subset)
        # x - y gives the sum of the other subset, so x - y - y is the difference of sum of the two subsets
        assert abs(x - y - y) == diff
