# bubble sort


def bubble_sort(nums, is_sorted, step):
    """
    args:
        nums is a given unsorted number list.
        is_sorted is a bloom flag
        step is nums's length.
    """

    if step is 1 or is_sorted:
        # nums is already sorted, so we can pass through the list len(nums) times
        return nums
    else:
        is_swapped = False
        for i in range(len(nums) - 1):
            # compare each pair of adjacent items and swaps them if they are in the wrong order
            if nums[i] > nums[i + 1]:
                is_swapped = True
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
            # if swapped is true, just pass through the list again
        print(nums)
        return bubble_sort(nums, not is_swapped, step - 1)


if __name__ == '__main__':

    l = [1, 9, 7, 10, 7, 5, 199, 5]
    print(bubble_sort(l, False, len(l)))

