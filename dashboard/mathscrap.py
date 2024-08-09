import math

def graph_numbers_in_column(number_of_graphs, column_number):
    number_of_columns = math.floor(number_of_graphs**0.5)
    number_of_rows = math.ceil(number_of_graphs / number_of_columns)
    graph_numbers = []
    for r in range(1, number_of_rows + 1):
        n = (r - 1) * number_of_columns + column_number
        if n <= number_of_graphs:
            graph_numbers.append(n)
    
    return graph_numbers

print(graph_numbers_in_column(number_of_graphs=9, column_number=1))


