class Queue:
    def __init__(self):
        self.queue = []
        self.length = 0

    def push(self, value):
        self.queue.append(value)
        self.length += 1

    def pop(self):
        if self.length > 0:
            self.length -= 1
            element = self.queue[0]
            self.queue = self.queue[1:]
            return element
        else:
            return None

    def peek(self):
        if self.length > 0:
            return self.queue[0]
        else:
            return None


queue = Queue()
queue.push(1)
queue.push(2)
queue.push("56")
print(queue.peek())
print(queue.pop())
print(queue.peek())
print()
queue2 = Queue()
queue2.push(1)
queue2.push("45")
print(queue2.peek())
print(queue2.pop())
print(queue2.peek())
print(queue2.pop())
print(queue2.peek())
print(queue2.pop())
print(queue.queue, queue2.queue)

