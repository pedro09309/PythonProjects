class Solution(object):
    def BinarySearch(self, nums: list[int], target: int) -> int:
        lowest = 0
        highest = len(nums) - 1
        index = -1

        # Find the target
        while lowest <= highest:
            mid = (lowest + highest) // 2

            if nums[mid] == target:
                index = mid  # Target is found!
                break
            elif nums[mid] < target:  # Search to the right
                lowest = mid + 1
            else:  # Search to the left
                highest = mid - 1

        # Return the index of the target, if found.
        return index


# TEST CASE
solution = Solution()
input = [-1,0,3,5,9,12]
target = 9
output = solution.BinarySearch(input, target)

print(f'Input: {input}')
print(f'Target: {target}')
print(f'Output: {output}')