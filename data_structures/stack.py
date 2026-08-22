"""
Stack Data Structure

A Stack is a linear data structure that follows the LIFO (Last In, First Out)
principle. The last element added is the first one to be removed.

Operations & Time Complexity:
    - Push:    O(1) — add element to top
    - Pop:     O(1) — remove element from top
    - Peek:    O(1) — view top element without removing
    - Search:  O(n)
    - isEmpty: O(1)

Space Complexity: O(n)

Real-world applications:
    - Undo/Redo functionality
    - Browser back/forward navigation
    - Expression evaluation (postfix, prefix)
    - Balanced parentheses checking
    - Function call stack (recursion)

>>> stack = Stack()
>>> stack.is_empty()
True

>>> stack.push(1)
>>> stack.push(2)
>>> stack.push(3)
>>> str(stack)
'Stack([1, 2, 3]) <- top'

>>> stack.peek()
3

>>> stack.pop()
3

>>> len(stack)
2
"""

from __future__ import annotations

from typing import Any


class Stack:
    """
    Stack implementation using a Python list.

    >>> s = Stack()
    >>> s.push(10)
    >>> s.push(20)
    >>> s.push(30)
    >>> s.pop()
    30
    >>> s.peek()
    20
    >>> len(s)
    2
    """

    def __init__(self, max_size: int | None = None) -> None:
        """
        Initialize an empty stack.

        Args:
            max_size: Optional maximum size. None means unlimited.
        """
        self._items: list[Any] = []
        self._max_size = max_size

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"Stack({self._items}) <- top"

    def __repr__(self) -> str:
        return f"Stack(items={self._items}, max_size={self._max_size})"

    def __contains__(self, item: Any) -> bool:
        """
        Check if an item is in the stack.

        >>> s = Stack()
        >>> s.push(42)
        >>> 42 in s
        True
        >>> 99 in s
        False
        """
        return item in self._items

    def __iter__(self):
        """
        Iterate over items from top to bottom.

        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.push(3)
        >>> list(s)
        [3, 2, 1]
        """
        return reversed(self._items)

    def is_empty(self) -> bool:
        """Return True if the stack is empty."""
        return len(self._items) == 0

    def is_full(self) -> bool:
        """Return True if the stack has reached its max size."""
        if self._max_size is None:
            return False
        return len(self._items) >= self._max_size

    def push(self, item: Any) -> None:
        """
        Push an item onto the top of the stack. O(1).

        Args:
            item: The item to push.

        Raises:
            OverflowError: If the stack is full (when max_size is set).

        >>> s = Stack(max_size=2)
        >>> s.push(1)
        >>> s.push(2)
        >>> s.is_full()
        True
        """
        if self.is_full():
            raise OverflowError(
                f"Stack is full (max_size={self._max_size})"
            )
        self._items.append(item)

    def pop(self) -> Any:
        """
        Remove and return the top item. O(1).

        Returns:
            The top item.

        Raises:
            IndexError: If the stack is empty.

        >>> s = Stack()
        >>> s.push(10)
        >>> s.push(20)
        >>> s.pop()
        20
        >>> s.pop()
        10
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """
        Return the top item without removing it. O(1).

        Returns:
            The top item.

        Raises:
            IndexError: If the stack is empty.

        >>> s = Stack()
        >>> s.push(42)
        >>> s.peek()
        42
        >>> len(s)
        1
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()

    def to_list(self) -> list:
        """
        Return a copy of the internal list (bottom to top).

        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.to_list()
        [1, 2]
        """
        return list(self._items)


# ─────────────────────────────────────────────────────────────
# Practical Applications
# ─────────────────────────────────────────────────────────────


def is_balanced_parentheses(expression: str) -> bool:
    """
    Check if parentheses/brackets in an expression are balanced.

    Uses a stack to match opening and closing brackets.

    Args:
        expression: A string containing brackets to check.

    Returns:
        True if all brackets are properly balanced.

    >>> is_balanced_parentheses("()")
    True

    >>> is_balanced_parentheses("([{}])")
    True

    >>> is_balanced_parentheses("([)]")
    False

    >>> is_balanced_parentheses("(()")
    False

    >>> is_balanced_parentheses("")
    True

    >>> is_balanced_parentheses("{[()]}")
    True
    """
    matching = {")": "(", "]": "[", "}": "{"}
    stack = Stack()

    for char in expression:
        if char in "({[":
            stack.push(char)
        elif char in ")}]":
            if stack.is_empty() or stack.pop() != matching[char]:
                return False

    return stack.is_empty()


def evaluate_postfix(expression: str) -> float:
    """
    Evaluate a postfix (Reverse Polish Notation) expression.

    Args:
        expression: Space-separated postfix expression.
                   Operators: +, -, *, /

    Returns:
        The result of the expression.

    >>> evaluate_postfix("2 3 +")
    5.0

    >>> evaluate_postfix("5 1 2 + 4 * + 3 -")
    14.0

    >>> evaluate_postfix("4 2 /")
    2.0

    >>> evaluate_postfix("3 4 * 2 5 * +")
    22.0
    """
    stack = Stack()
    operators = {"+", "-", "*", "/"}

    for token in expression.split():
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.push(a + b)
            elif token == "-":
                stack.push(a - b)
            elif token == "*":
                stack.push(a * b)
            elif token == "/":
                stack.push(a / b)
        else:
            stack.push(float(token))

    return stack.pop()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo: Basic stack operations
    print("=== Stack Demo ===")
    stack = Stack()
    for val in [10, 20, 30, 40]:
        stack.push(val)
        print(f"Pushed {val}: {stack}")

    print(f"\nPeek: {stack.peek()}")
    print(f"Pop:  {stack.pop()}")
    print(f"After pop: {stack}")

    # Demo: Balanced parentheses
    print("\n=== Balanced Parentheses ===")
    test_cases = ["(())", "([{}])", "([)]", "(()", "{[()]}"]
    for expr in test_cases:
        result = "✓ balanced" if is_balanced_parentheses(expr) else "✗ unbalanced"
        print(f"  '{expr}' → {result}")

    # Demo: Postfix evaluation
    print("\n=== Postfix Evaluation ===")
    expressions = [
        ("2 3 +", "2 + 3"),
        ("5 1 2 + 4 * + 3 -", "5 + (1+2)*4 - 3"),
        ("3 4 * 2 5 * +", "3*4 + 2*5"),
    ]
    for postfix, infix in expressions:
        result = evaluate_postfix(postfix)
        print(f"  {postfix} = {result}  (infix: {infix})")
