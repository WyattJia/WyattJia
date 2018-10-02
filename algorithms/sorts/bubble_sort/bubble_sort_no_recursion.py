# bubble_sort

def bubble_sort(nums):
    counts = len(nums)
    for i in range(0, counts):
        for j in range(i + 1, counts):
            if nums[i] > nums[j]:
                nums[i], nums[j] = nums[j], nums[i]

    return nums

if __name__ == '__main__':
    l = [1, 9, 7, 10, 7, 5, 199, 5]
    assert bubble_sort(l) == [1, 5, 5, 7, 7, 9, 10, 199]
    print(bubble_sort(l))


