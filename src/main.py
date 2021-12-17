from src.tree.rb_tree import RedBlackTree


if __name__ == '__main__':

    tree1 = RedBlackTree([18, 15, 8, 5, 17])
    tree1.print_tree()

    node = tree1.find_node(8)

    print(tree1.get_height())
    print(tree1.get_black_height())
    print("\n---------------------")

    tree2 = RedBlackTree()

    tree2.insert(55)
    tree2.insert(40)
    tree2.insert(65)
    tree2.insert(60)
    tree2.insert(75)
    tree2.insert(57)

    tree2.print_tree()

    tree2.delete_node(40)

    print(tree2.get_height())
    print(tree2.get_black_height())

    tree2.print_tree()

