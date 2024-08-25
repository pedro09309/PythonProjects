class Solution:
    def isHappy(self, n: int) -> bool:
        res = 0

        while n > 0:
            res += (n % 10)**2
            n = (n // 10)
        
        if (res == 1)  or (res == 7): return True
        elif (res < 10)             : return False
        else                        : return self.isHappy(res)

# TEST CASE
solution = Solution()
input = 19
output = solution.isHappy(input)

print(f'Input: {input}')
print(f'Output: {output}')