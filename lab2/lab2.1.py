import sys
from typing import List, Union, Any

class SimpleLispTranslator:
    def __init__(self):
        self.output_lines = []

    def tokenize(self, chars: str) -> List[str]:
        # преобразование строки в список токенов
        return chars.replace('(', ' ( ').replace(')', ' ) ').split()

    def parse(self, tokens: List[str]) -> Any:
        if not tokens:
            raise SyntaxError("Неожиданный конец программы")
        
        token = tokens.pop(0)
        
        if token == '(':
            ast = []
            while tokens[0] != ')':
                ast.append(self.parse(tokens))
            tokens.pop(0)  # удаляем закрывающую скобку
            return ast
        elif token == ')':
            raise SyntaxError("Неожиданная ')'")
        else:
            return self._atom(token)

    def _atom(self, token: str) -> Union[int, float, str]:
        # определение типа токена: число или строка
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token

    def translate_node(self, node: Any) -> str:
        match node:
            # присваивание (set x 10)
            case ['set', var_name, value]:
                val_code = self.translate_node(value)
                return f"{var_name} = {val_code}"

            # арифметика (+ 1 2) или (* x 5)
            case [op, left, right] if op in ('+', '-', '*', '/'):
                l_code = self.translate_node(left)
                r_code = self.translate_node(right)
                return f"({l_code} {op} {r_code})"

            # вывод (print x "hello")
            case ['print', *args]:
                args_code = ", ".join([str(self.translate_node(arg)) for arg in args])
                return f"print({args_code})"

            # если это просто значение (число или строка)
            case _:
                if isinstance(node, str) and not node.replace('.', '', 1).isdigit():
                    return node
                return str(node)

    def compile(self, source_code: str) -> str:
        """Главный метод: токенизация -> парсинг -> трансляция."""
        tokens = self.tokenize(source_code)
        python_code = []
        
        while tokens:
            ast = self.parse(tokens)
            translated_line = self.translate_node(ast)
            python_code.append(translated_line)
            
        return "\n".join(python_code)

lisp_code = """
(set x 10)
(set y 20
(set result (+ x y))
(print result)
(print (+ result 5))
"""

translator = SimpleLispTranslator()
python_result = translator.compile(lisp_code)

print("Исходный код (Lisp)")
print(lisp_code.strip())
print("\nРезультат трансляции (Python)")
print(python_result)

print("\nВыполнение полученного кода")
exec(python_result)
