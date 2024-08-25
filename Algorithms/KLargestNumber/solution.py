class Solution:
    def kLargest(self,arr, n, k):
        # Sort in ascending order (selection sort)
        for i in range(n):
            
            lowest_pos = i
            
            for j in range(i + 1, n):
                if(arr[j] < arr[lowest_pos]):
                    lowest_pos = j
            
            arr[i], arr[lowest_pos] = arr[lowest_pos], arr[i]
        
        # Chop the array to get the k largest elements     
        new_arr = [0] * k
        for i in range(k):
            new_arr[i] = arr[(n - 1) - i]
        
        return new_arr

# TEST CASE
solution = Solution()
input = [1, 23, 12, 9, 30, 2, 50]
k = 3
output = solution.kLargest(input, 7, 3)

print(f'Input: {input}')
print(f'Output: {output}')