from datetime import datetime

ast_watered = datetime.strptime(
    "Mon, 05 Aug 2024 14:56:47 GMT", "%a, %d %b %Y %H:%M:%S %Z")
print(ast_watered)
