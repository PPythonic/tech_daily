class Node(object):
    """
        节点基本类
    """
    def __init__(self, item):
        self.item = item  # 该节点值
        self.prev = None  # 上一个节点
        self.next = None   # 下一个节点


class DoubleLoopLinkedChain(object):
    """
        双向循环链表类
    """
    def __init__(self):
        self.__head = None

    @property
    def is_empty(self):
        """
            判断链表是否为空
        """
        return self.__head is None

    @property
    def length(self):
        """
            链表的长度
        """
        if self.is_empty:
            return 0
        else:
            cur = self.__head
            n = 1
            while cur.next is not self.__head:
                cur = cur.next
                n += 1
            return n

    @property
    def loop(self):
        """
            遍历链表内元素
        """
        if self.is_empty:
            raise ValueError("ERROR NULL")
        else:
            print(self.__head.item)
            cur = self.__head.next
            while cur != self.__head:
                print(cur.item)
                cur = cur.next

    def add(self, item):
        """
            链表头部插入节点
        """
        node = Node(item)
        if self.is_empty:
            self.__head = node
            node.prev = node
            node.next = node
        else:
            node.next = self.__head
            node.prev = self.__head.prev
            self.__head.prev.next = node
            self.__head.prev = node
            self.__head = node
        print("add {} Success".format(item))

    def append(self, item):
        """
            链表尾部追加节点
        """
        if self.is_empty:
            self.add(item)
        else:
            node = Node(item)
            node.prev = self.__head.prev
            node.next = self.__head
            self.__head.prev.next = node
            self.__head.prev = node
        print("append {} Success".format(item))

    def insert(self, pos, item):
        """
            指定位置插入链表
        """
        if pos <= 0:
            self.add(item)
        elif pos >= self.length - 1:
            self.append(item)
        else:
            index = 0
            cur = self.__head
            node = Node(item)
            while index < pos - 1:
                cur = cur.next
                index += 1
            node.prev = cur
            node.next = cur.next
            cur.next.prev = node
            cur.next = node

    def remove(self, item):
        """
            删除节点
        """
        if self.is_empty:
            raise ValueError("ERROR VALUE")
        else:
            cur = self.__head
            if cur.item == item:
                if self.length == 1:
                    self.__head = None
                else:
                    self.__head.prev.next = cur.next
                    self.__head.next.prev = cur.prev
                    self.__head = cur.next
            else:
                cur = cur.next
                while cur is not self.__head:
                    if cur.item != item:
                        cur = cur.next
                    else:
                        cur.prev.next = cur.next
                        cur.next.prev = cur.prev
                        return
                raise ValueError("Not this Item {}".format(item))

    def exit(self, item):
        """
            判断链表中是否存在指定元素
        """
        if self.is_empty:
            return False
        else:
            cur = self.__head
            if cur.item == item:
                return True
            while cur.next is not self.__head:
                if cur.item == item:
                    return True
                cur = cur.next
            if cur.item == item:
                return True
            return False 


if __name__ == '__main__':
    chain = DoubleLoopLinkedChain()
    # print(chain.exit(1))
    chain.add(1)
    # print(chain.exit(1))
    chain.add(2)
    chain.append(3)
    # print(chain.length)
    chain.insert(1, 4)
    chain.remove(1)
    chain.loop
    print("chain length -> {}".format(chain.length))
