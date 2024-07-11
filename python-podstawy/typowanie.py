def greet(name: str) -> str:
    return "Hello, " + name

message: str = "Hello, world!"
message = 42  # Błąd: Typ 'int' nie może być przypisany do typu 'str' (w trakcie analizy statycznej, ale nie w trakcie wykonywania)
# analiza statyczna: pylint typowanie.py, wykrywanie błędów typowania: mypy typowanie.py