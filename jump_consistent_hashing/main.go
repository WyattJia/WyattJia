package main

import (
	"math/rand"
)

/*
开始桶的总数为1，所有的key都放在第0个桶中。
然后每增加一个桶，生成一个随机数，
当这个随机数为奇数时，将key放在保持在原始桶中，
当这个key为偶数时，将key移动到新增的桶中。
*/
func consistentHashOne(key int, n int) int {
	/* 使用 key 作为随机数的种子，
       一旦 key 和 n 确定了，
	函数的返回值也是固定的，
	并且当函数参数为 n 和参数为 n - 1 时，
	循环过程中的前面几步生成的随机数都是一样的。
	*/
	rand.Seed(int64(key))
	id := 0
	for i := 1; i < n; i ++ {
		// 每增加一个桶，生成一个随机数
		if rand.Uint64() % 2 == 1 {
			// 如果随机数是奇数，key 保留在原来的桶中
			id = id
		} else {
			// 如果随机数是偶数，key 移动到新分配的桶中
			id = i
		}
	}
	return id
}


/*
开始桶的总数为1，所有的key都放在第0个桶中，
同时生成一个大于当前桶数的随机数。
每增加一个新桶时，判断当前桶总数是否超过这个随机数。
如果未超过（桶数小于或等于这个随机数），则将key保留在原来的桶中；
如超过，则将key移动到新增加的桶中，同时重新生成一个大于当前桶数的随机数，
后续增加新桶时，使用和前面相同的逻辑进行判断。
*/
func consistentHashTwo(key int, n int) int {
    rand.Seed(int64(key))
    id := 0
    // 生成一个随机数 fence
    fence := rand.Int()
    for n > fence {
    	id = fence
    	fence = id + rand.Int()
	}
	return id
}

func main()  {
	consistentHashOne(rand.Int(), 1)
	consistentHashTwo(rand.Int(), 1)
}
