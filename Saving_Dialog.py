PATH = 'saving.txt'
saving = open(PATH, 'w')
string = ''


class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


class Queue:
    def __init__(self):
        self.head = None
        self.lens = 0

    def push(self, text):
        self.lens += 1
        if self.head is None:
            self.head = Node(text)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(text)

    def pop(self):  # return first num from queue and delete this one
        if self.lens > 1:
            info = self.head.value
            self.head = Node(self.head.next.value, self.head.next.next)
            self.lens -= 1
            return info
        elif self.lens == 1:
            info = self.head.value
            self.head = None
            self.lens -= 1
            return info
        else:
            return False

    def empty(self):
        return self.lens == 0

    def size(self):
        return self.lens


def clean_data():  # удаление из файла
    with open(PATH, 'w') as deleter:
        pass


def saving_on_file(element):
        while True:
            line = element.pop()
            if line is not False:
                if line is not None:
                    saving.write(line)
            else:
                break