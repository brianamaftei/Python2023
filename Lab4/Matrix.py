class Matrix:
    def __init__(self, N, M):
        self.matrix = list(list(0 for _ in range(M)) for _ in range(N))
        self.N = N
        self.M = M

    def get(self, i, j):
        if i < 0 or i >= self.N or j < 0 or j >= self.M:
            return None
        return self.matrix[i][j]

    def set(self, i, j, value):
        if i < 0 or i >= self.N or j < 0 or j >= self.M:
            return None
        self.matrix[i][j] = value

    def transpose(self):
        transpose_matrix = Matrix(self.M, self.N)
        for i in range(self.N):
            for j in range(self.M):
                transpose_matrix.matrix[j][i] = self.matrix[i][j]
        return transpose_matrix.matrix

    def transpose_1(self):
        lists = self.matrix
        max_length = max([len(lst) for lst in lists])
        return list(map(list, zip(*list(lst + [None] * (max_length - len(lst)) for lst in lists))))

    def modify_all(self, lambda_function):
        new_matrix = Matrix(self.N, self.M)
        new_matrix.matrix = [[lambda_function(self.matrix[row][column]) for column in range(self.M)] for row in
                             range(self.N)]
        return new_matrix.matrix

    def multiplication(self, matrix):
        if self.M != matrix.N:
            return None

        new_matrix = Matrix(self.N, matrix.M)
        for i in range(self.N):
            for j in range(matrix.M):
                for k in range(self.M):
                    el1 = self.matrix[i][k]
                    el2 = matrix.matrix[k][j]
                    if type(el1) is not int or type(el2) is not int:
                        return None
                    new_matrix.matrix[i][j] += self.matrix[i][k] * matrix.matrix[k][j]
        return new_matrix.matrix


transform = lambda string: string[-1] in "2468"


def zip_of_lists(*lists):
    max_length = max([len(lst) for lst in lists])
    return list(map(list, zip(*list(lst + [None] * (max_length - len(lst)) for lst in lists))))


matrix1 = Matrix(4, 3)
matrix1.set(0, 0, "0")
matrix1.set(0, 1, "1")
matrix1.set(0, 2, "2")
matrix1.set(1, 0, "3")
matrix1.set(1, 1, "4")
matrix1.set(1, 2, "5")
matrix1.set(2, 0, "6")
matrix1.set(2, 1, "7")
matrix1.set(2, 2, "8")
matrix1.set(3, 0, "9")
matrix1.set(3, 1, "10")
matrix1.set(3, 2, "11")

print(matrix1.matrix)
print(matrix1.get(0, 0))
print(matrix1.get(0, 1))
print(matrix1.transpose())
print(matrix1.transpose_1())
print(matrix1.modify_all(transform))

matrix2 = Matrix(3, 2)
matrix2.set(0, 0, 1)
matrix2.set(0, 1, 2)
matrix2.set(1, 0, 3)
matrix2.set(1, 1, 4)
matrix2.set(2, 0, 5)
matrix2.set(2, 1, 6)
print(matrix2.matrix)

matrix3 = Matrix(4, 3)
matrix3.set(0, 0, 0)
matrix3.set(0, 1, 1)
matrix3.set(0, 2, 2)
matrix3.set(1, 0, 3)
matrix3.set(1, 1, 4)
matrix3.set(1, 2, 5)
matrix3.set(2, 0, 6)
matrix3.set(2, 1, 7)
matrix3.set(2, 2, 8)
matrix3.set(3, 0, 9)
matrix3.set(3, 1, 10)
matrix3.set(3, 2, 11)
print(matrix3.matrix)
print(matrix3.multiplication(matrix2))
