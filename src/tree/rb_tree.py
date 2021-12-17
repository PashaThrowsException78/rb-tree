# Implementing Red-Black Tree in Python


import sys


class Node:
    def __init__(self, value):
        self.value = value
        self.parent: Node = None
        self.left: Node = None
        self.right: Node = None
        self.is_red = False


#  rb-tree implementation (min values left) based on linked list concept
class RedBlackTree:
    def __init__(self, values: list = None):
        if values is None:
            values = []
        self.nil = Node(0)
        self.nil.is_red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
        if values is not None and len(values) > 0:
            for i in range(len(values)):
                self.insert(values[i])

    def __preorder_helper(self, node):
        if node != self.nil:
            sys.stdout.write(node.value + " ")
            self.__preorder_helper(node.left)
            self.__preorder_helper(node.right)

    def __inorder_helper(self, node):
        if node != self.nil:
            self.__inorder_helper(node.left)
            sys.stdout.write(node.value + " ")
            self.__inorder_helper(node.right)

    def __postorder_helper(self, node):
        if node != self.nil:
            self.__postorder_helper(node.left)
            self.__postorder_helper(node.right)
            sys.stdout.write(node.value + " ")

    #  return node with requested value, start searching from transmitted node
    def __search_tree_helper(self, node, key):
        if node == self.nil or key == node.value:
            return node

        if key < node.value:
            return self.__search_tree_helper(node.left, key)
        return self.__search_tree_helper(node.right, key)

    #  balancing the tree after deletion
    def __delete_fix(self, x):
        while x != self.root and not x.is_red:
            if x == x.parent.left:
                s = x.parent.right
                if s.is_red is True:
                    s.is_red = False
                    x.parent.is_red = True
                    self.__left_rotate(x.parent)
                    s = x.parent.right

                if not s.left.is_red and not s.right.is_red:
                    s.is_red = True
                    x = x.parent
                else:
                    if not s.right.is_red:
                        s.left.is_red = False
                        s.is_red = True
                        self.__right_rotate(s)
                        s = x.parent.right

                    s.is_red = x.parent.is_red
                    x.parent.is_red = False
                    s.right.is_red = False
                    self.__left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.is_red:
                    s.is_red = False
                    x.parent.is_red = True
                    self.__right_rotate(x.parent)
                    s = x.parent.left

                if not s.right.is_red and not s.right.is_red:
                    s.is_red = True
                    x = x.parent
                else:
                    if not s.left.is_red:
                        s.right.is_red = False
                        s.is_red = True
                        self.__left_rotate(s)
                        s = x.parent.left

                    s.is_red = x.parent.is_red
                    x.parent.is_red = False
                    s.left.is_red = False
                    self.__right_rotate(x.parent)
                    x = self.root
        x.is_red = False

    # swap nodes' positions
    def __rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

        if u.value == 0:
            print("\During another operation, swapped NILL with \"" + str(v.value) + "\":")
            self.__print_helper(self.root, "", True, 0)
        elif v.value == 0:
            print("\nDuring another operation, swapped \"" + str(u.value) + "\" with NILL:")
            self.__print_helper(self.root, "", True, 0)
        else:
            print("\nDuring another operation, swapped nodes \"" + str(u.value) + "\" and \"" + str(v.value) + "\":")
            self.__print_helper(self.root, "", True, 0)

    def __delete_node_helper(self, node, key):
        z = self.nil
        while node != self.nil:
            if node.value == key:
                z = node

            if node.value <= key:
                node = node.right
            else:
                node = node.left

        if z == self.nil:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.is_red
        if z.left == self.nil:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.__minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.is_red
        if y_original_color == 0:
            self.__delete_fix(x)

    # balance the tree after insertion
    def __fix_insert(self, node: Node):
        while node.parent.is_red:
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.is_red:
                    u.is_red = False
                    node.parent.is_red = False
                    node.parent.parent.is_red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.__right_rotate(node)
                    node.parent.is_red = False
                    node.parent.parent.is_red = True
                    self.__left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u.is_red:
                    u.is_red = False
                    node.parent.is_red = False
                    node.parent.parent.is_red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.__left_rotate(node)
                    node.parent.is_red = False
                    node.parent.parent.is_red = True
                    self.__right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.is_red = False

    # printing the tree
    def __print_helper(self, current, indention, child_r, check):
        if current is not self.nil:
            print(indention, end='')
            if not child_r:
                print("L-----", end='')
                indention += "|     "
            else:
                if current.value == self.root.value and check == 0:
                    print("V-----", end='')
                    check = 1
                else:
                    print("R-----", end='')
                indention += "      "
            print(current.value, end=' ')
            if current.is_red:
                print("(RED)")
            else:
                print("(BLACK)")
            self.__print_helper(current.left, indention, False, check)
            self.__print_helper(current.right, indention, True, check)

    def preorder(self):
        self.__preorder_helper(self.root)

    def inorder(self):
        self.__inorder_helper(self.root)

    def postorder(self):
        self.__postorder_helper(self.root)

    def find_node(self, value):
        if value is None:
            return None
        return self.__search_tree_helper(self.root, value)

    #  find min node in the same branch with transmitted node
    def __minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    #  find min value in tree
    def minimum(self):
        node = self.root
        while node.left != self.nil:
            node = node.left
        return node.value

    #  find max node in the same branch with transmitted node
    def __maximum(self, node):
        while node.right != self.nil:
            node = node.right
        return node

    #  find max value in tree
    def maximum(self):
        node = self.root
        while node.right != self.nil:
            node = node.right
        return node.value

    def __successor(self, x):
        if x.right != self.nil:
            return self.__minimum(x.right)

        y = x.parent
        while y != self.nil and x == y.right:
            x = y
            y = y.parent
        return y

    def __predecessor(self, x):
        if x.left != self.nil:
            return self.__maximum(x.left)

        y = x.parent
        while y != self.nil and x == y.left:
            x = y
            y = y.parent

        return y

    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        print("\nleft-rotated tree in \"" + str(x.value) + "\":")
        self.__print_helper(self.root, "", True, 0)

    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        print("\nright-rotated tree in \"" + str(x.value) + "\":")
        self.__print_helper(self.root, "", True, 0)

    def insert(self, key):
        if key is None:
            raise ValueError("Unable to insert None to tree!")
        print("\ninserting \"" + str(key) + "\":")
        node = Node(key)
        node.parent = None
        node.value = key
        node.left = self.nil
        node.right = self.nil
        node.is_red = True

        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.value < x.value:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.value < y.value:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.is_red = False
            self.__print_helper(self.root, "", True, 0)
            print("\n")
            return

        if node.parent.parent is None:
            self.__print_helper(self.root, "", True, 0)
            print("\n")
            return

        self.__fix_insert(node)
        self.__print_helper(self.root, "", True, 0)
        print("\n")

    def get_root(self):
        return self.root

    def delete_node(self, value):
        if value is None:
            return
        self.__delete_node_helper(self.root, value)
        print("\ndeleted \"" + str(value) + "\" from tree:")
        self.__print_helper(self.root, "", True, 0)

    def print_tree(self):
        print("\ntree:")
        self.__print_helper(self.root, "", True, 0)

    def __height_helper(self, node):
        if node is not self.nil:
            return max(self.__height_helper(node.left), self.__height_helper(node.right)) + 1
        else:
            return 0

    def get_height(self, node=None):
        if node is None:
            node = self.root
        return self.__height_helper(node)

    def __black_height_helper(self, node):
        if node is not self.nil:
            h = max(self.__black_height_helper(node.left), self.__black_height_helper(node.right))
            if node.is_red:
                return h
            else:
                return h + 1
        else:
            return 0

    def get_black_height(self, node=None):
        if node is None:
            node = self.root
        return self.__black_height_helper(node)
