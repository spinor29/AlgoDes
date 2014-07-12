# Quicksort in Julia

function quicksort(numbers, i_start, i_end)
    if i_start >= i_end
        return
	end
	
    n = i_end - i_start + 1
	
	# Use the median among first, middle, and last elements as the pivot
	i_middle = int(i_start + n / 2 + n % 2 - 1)
	a = numbers[i_start]; b = numbers[i_middle]; c = numbers[i_end]
	i_swap = 0
	if a < b & a < c
	    i_swap = b < c ? i_middle : i_end
	    numbers[i_start], numbers[i_swap] = numbers[i_swap], numbers[i_start]
	elseif a > b & a > c
	    i_swap = b > c ? i_middle : i_end
		numbers[i_start], numbers[i_swap] = numbers[i_swap], numbers[i_start]
	end
	
	pivot = numbers[i_start]
	
    u = i_start # position of the boundary between left and right partitions
    
	for j in (i_start+1):i_end
        if numbers[j] <= pivot
		    u += 1
            if j > u
                numbers[u], numbers[j] = numbers[j], numbers[u] # swap
		    end
	    end
	end
	
	if u > i_start
	    numbers[i_start], numbers[u] = numbers[u], numbers[i_start]
	    quicksort(numbers, i_start, u-1)
		if u < (i_end-1); quicksort(numbers, u+1, i_end); end
	else
	    quicksort(numbers, u+1, i_end)
	end
	
	return
end

num_count = 20000
integers = [1:num_count]
integers = reverse(integers)
println(@elapsed quicksort(integers, 1, num_count))
println(integers)


