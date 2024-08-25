
#0 (n^4) time | O(n^3) space - where n is the height and width of the matrix
def squareOfZeroes (matrix):
    lastIdx = len(matrix) - 1
    return hasSquareOfZeroes (matrix, 0, 0, lastIdx, lastIdx, {})

#r1 is the top row, c1 is the left column
# r2 is the bottom row, c2 is the right column
def hasSquareOfZeroes (matrix, r1, c1, r2, c2, cache):
    if r1 >= r2 or c1 >= c2:
        return False
    
    key = str(r1) + "-" + str(c1) + "-" + str(r2) + "-" + str(c2)
    if key in cache:
        return cache [key]

    cache[key] = (
        isSquareOfZeroes(matrix, r1, c1, r2, c2)
        or hasSquareOfZeroes(matrix, r1 + 1, c1 + 1, r2 - 1, c2 -1, cache)
        or hasSquareOfZeroes(matrix, r1, c1 + 1, r2 - 1, c2, cache)
        or hasSquareOfZeroes(matrix, r1 + 1, c1, r2, c2 -1, cache) 
        or hasSquareOfZeroes(matrix, r1 + 1, c1 + 1, r2, c2, cache)
        or hasSquareOfZeroes(matrix, r1, c1, r2 - 1, c2 - 1, cache)
    )
    return cache [key]

# r1 is the top row, c1 is the left column 
# r2 is the bottom row, c2 is the right column
def isSquareOfZeroes (matrix, r1, c1, r2, c2): 
    for row in range(r1, r2 + 1):
        if matrix[row][c1] != 0 or matrix[row][c2] != 0: 
            return False
    for col in range(c1, c2 + 1):
        if matrix[r1][col] != 0 or matrix[r2][col] != 0: 
            return False
    return True

# TEST
# input = [
#     [ , , , , , ],
#     [0,0,0,0,0, ],
#     [0, , , ,0, ],
#     [0, , , ,0, ],
#     [0, , , ,0, ],
#     [0,0,0,0,0, ],
# ]
input = [[1,1,1,0,1,0],[0,0,0,0,0,1],[0,1,1,1,0,1],[0,0,0,1,0,1],[0,1,1,1,0,1],[0,0,0,0,0,1]]
output = squareOfZeroes(input)

print(f'Input: ')
for i in range(len(input)):
    print(f'{input[i]}')

print(f'Output: {output}')
