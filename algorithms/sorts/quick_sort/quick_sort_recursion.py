# quick sort

import random


def quick_sort(nums):
    if len(nums) < 2:
        return nums
    else:
        pivot = nums[0]
        smaller = [i for i in nums[1:] if i <= pivot]
        bigger = [i for i in nums[1:] if i > pivot]
        result = quick_sort(smaller) + [pivot] + quick_sort(bigger)
        return result


if __name__ == '__main__':
   l = [random.randint(10, 10000) for i in range(10)]
   print(l)
   print(quick_sort(l))
