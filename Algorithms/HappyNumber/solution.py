class Solution:
    def isHappy(self, n: int) -> bool:
        res = 0

        for i in range(n):
            res += (n % 10)**2
            n = (n // 10)
        
        if res == 1     : return True
        elif (res >= 10): return self.isHappy(res)
        else            : return False


# TEST CASE
solution = Solution()
input = 19
output = solution.isHappy(input)

print(f'Input: {input}')
print(f'Output: {output}')