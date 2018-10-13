import os

sorts = ['bubble_sort', 'insert_sort', 'selection_sort', 'merge_sort', 'quick_sort']

is_recursion = ['_recursion', '_no_recursion']

binary_trees = ['binary_tree_high', 'BFS', 'binary_tree_to_linked_list',
                'is_avl', 'is_complete', 'binary_tree_node_sum',
                'are_same_tree', 'pre_order', 'in_order', 'post_order']

searchs = ['binary_search', 'binary_search_tree']

data_structures = ['list', 'linked_list', 'hash_table', 'array',
                   'Intersection_of_Two_Linked_Lists', 'merge_sorted_list', 'queue',
                   'stack', 'Reverse_Linked_List', ]

DPs_and_greedy = ['coin_change', 'backpack', 'fiboncci_sum', 'fibonacci_rabbit']

pwd_path = os.getcwd()
sorts_path = pwd_path + '/sorts'


def create_sort_folder(sorts_path):
    if not os.path.isdir(sorts_path):
        os.mkdir(sorts_path)

    for i in sorts:
        os.mkdir(sorts_path + '/' + i)

    return 'ok'


def create_sort_files(sorts_path):
    for i in sorts:
        for j in is_recursion:
            file = open(sorts_path + '/' + i + '/' + i + j + '.py', 'w')
            file.close()

    return 'ok'


def create_dps_and_greedy():
    os.mkdir(pwd_path + '/DPs_and_greedy')

    for i in DPs_and_greedy:
        os.mkdir(pwd_path + '/DPs_and_greedy' + '/' + i)

    for i in DPs_and_greedy:
        for j in is_recursion:
            file = open(pwd_path + '/DPs_and_greedy' + '/' + i + '/' + i + j + '.py', 'w')
            file.close()

    return 'ok'


def create_others():
    os.mkdir(pwd_path + '/data_structures')
    os.mkdir(pwd_path + '/binary_trees')
    for i in binary_trees:
        file = open(pwd_path + '/binary_trees/' + i + '.py', 'w')
        file.close()
    for i in data_structures:
        file = open(pwd_path + '/data_structures/' + i + '.py', 'w')
        file.close()
    return 'ok'


def create_searchs():
    os.mkdir(pwd_path + '/searchs')
    for i in searchs:
        os.mkdir(pwd_path + '/searchs/' + i)

    for i in searchs:
        for j in is_recursion:
            file = open(pwd_path + '/searchs/' + i + '/' + i + j + '.py', 'w')
            file.close()
    return 'ok'


if __name__ == '__main__':
    create_sort_folder(sorts_path)

    create_sort_files(sorts_path)

    create_dps_and_greedy()
    create_others()
    create_searchs()
