//  Quicksort in Swift
//  Created by Jong Lin on 6/4/14.
//  Copyright (c) 2014 Jong Lin. All rights reserved.
//

import Foundation

func quicksort(numbers: Int[], i_start: Int, i_end: Int) -> Int {
    if i_start >= i_end {
        return 0
    }

    let n = i_end - i_start + 1
    let m = 3 // pivot option 3: use the median among first, middle, and last element as the pivot
    var pivot: Int

    switch m {
    case 2:
        // Set the last element in the list as the pivot
        swap(&numbers[i_start], &numbers[i_end])
        
    case 3:
        // Set the median among first, middle, and last element in the list as the pivot
        let i_middle = i_start + n / 2 + (n % 2) - 1
        var i_swap: Int
        let a = numbers[i_start], b = numbers[i_middle], c = numbers[i_end]
        if a < b && a < c {
            i_swap = b < c ? i_middle : i_end
            swap(&numbers[i_start],&numbers[i_swap])
        }
        else if a > b && a > c {
            i_swap = b > c ? i_middle : i_end
            swap(&numbers[i_start],&numbers[i_swap])
        }

    default:
        // Do nothing. First element in the list is the pivot.
        break
    }
    
    pivot = numbers[i_start]

    var u = i_start // position of the interface between two partitions
    
    for j in (i_start+1)..(i_end+1) {
        if numbers[j] < pivot {
            ++u
            if j > u {
                swap(&numbers[u], &numbers[j])
            }
        }
    }

    if u > i_start {
        swap(&numbers[i_start], &numbers[u])
        quicksort(numbers, i_start, u-1)
        if u < (i_end-1) { quicksort(numbers, u+1, i_end) }
    }
    else { quicksort(numbers, u+1, i_end) }
    
    return
}

let num_count = 5000

var integers = Int[](count: num_count, repeatedValue: 0)
for i in 0..num_count {
    integers[i] = num_count-i
}

var n_comp = 0

n_comp = quicksort(integers, 0, (num_count-1))
println(integers)

// the built-in sort function seems to have problems sorting large numbers
//var sorted_int = sort(integers)

