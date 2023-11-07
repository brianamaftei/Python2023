class Stack:
    def __init__(self):
        self.stack = []
        self.length = 0

    def push(self, value):
        self.stack.append(value)
        self.length += 1

    def pop(self):
        if self.length > 0:
            self.length -= 1
            element = self.stack[-1]
            self.stack = self.stack[:-1]
            return element
        else:
            return None

    def peek(self):
        if self.length > 0:
            return self.stack[-1]
        else:
            return None


stack = Stack()
stack.push(1)
stack.push(2)
stack.push("56")
print(stack.peek())
print(stack.pop())
print(stack.peek())
print()
stack2 = Stack()
stack2.push(1)
stack2.push("45")
print(stack2.peek())
print(stack2.pop())
print(stack2.peek())
print(stack2.pop())
print(stack2.peek())
print(stack2.pop())
print(stack.stack, stack2.stack)
