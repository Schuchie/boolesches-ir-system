def levenshtein_distance(s, t):
    m = len(s)
    n = len(t)

    # matrix is a table with m+1 rows and n+1 columns
    matrix = [[0 for col in range(n+1)] for row in range(m+1)]

    for i in range(m+1):
        matrix[i][0] = i

    for j in range(n+1):
        matrix[0][j] = j

    for i in range(m+1):
        for j in range(n+1):
            # cost = 0 -> leave unchanged
            # cost = 1 -> substitution
            cost = 0 if s[i-1] == t[j-1] else 1

            matrix[i][j] = min(
                matrix[i-1][j] + 1,  # deletion
                matrix[i][j-1] + 1,  # insertion
                matrix[i-1][j-1] + cost,  # leave unchanged or substitution
            )

    return matrix[m][n]
