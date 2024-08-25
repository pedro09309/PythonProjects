# Steps to solve the problem:
# 1 - Get the complement of i-th elements;
# 2 - Search for the complement starting from i-th position

class Solution(object):
    def twoSum(self, nums, target):
    
        result = []
        complements = []

        for i in range(len(nums)):

            complement = target - nums[i]
            complements.append(complement)

            for k in range(i + 1, len(nums)):

                if(nums[k] == complements[i]):
                    result.append(i)
                    result.append(k)
                    break
                    
        return result

# TEST CASE
solution = Solution()
input = [2,7,11,15]
target = 9
output = solution.twoSum(input, target)

print(f'Input: {input}')
print(f'Target: {target}')
print(f'Output: {output}')