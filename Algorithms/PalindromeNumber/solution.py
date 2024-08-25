class Solution(object):
    def isPalindrome(self, x):
        result = False

        if x > -1:
            x_str  = str(x)
            x_size = len(x_str)

            for i in range(x_size):
                j = (x_size -1) - i
                if ((i != 0) and (i == j)):
                    break
                else:
                    if(x_str[i] == x_str[j]):
                        result = True
                    else:
                        result = False
                        break

        return result

# TEST CASE
solution = Solution()
input = 121
output = solution.isPalindrome(input)

print(f'Input: {input}')
print(f'Output: {output}')