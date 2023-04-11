class Hierarchy:
    def __init__(self, filename=None):
        self.hierarchy = None
        if filename is not None:
            self.init_from_file(filename)

    def init_from_file(self, filename: str):
        self.hierarchy = dict()
        last_on_level = [-1]
        # read file line by line
        with open(filename, 'r') as f:
            for line in f:
                tabs = line.count('\t')
                line = line.replace('\t', '')
                line = line.replace('\n', '')
                while tabs >= len(last_on_level):
                    last_on_level.append(-1)
                while (tabs + 1) < len(last_on_level):
                    last_on_level.pop()
                last_on_level[-1] += 1
                # add to hierarchy
                self.hierarchy[line] = last_on_level.copy()

    def write_to_file(self, filename: str):
        self.hierarchy.sort(key=lambda x: x.place)
        with open(filename, 'w') as f:
            for i in self.hierarchy:
                f.write('\t' * (len(i[1]) - 1) + i[0] + '\n')

    # def add_user(self, user_name: str, place: list):


def generate_resources_rights(hierarchy: list, filename: str):
    resources = []
    with open(filename, 'r') as f:
        for line in f:
            resources.append(line.replace('\n', ''))
    with open(str(filename.split('.')[0] + '&rights.txt'), 'w') as f:
        for i, r in enumerate(resources):
            f.write(r + '\t')
            for j, l in enumerate(hierarchy):
                if i >= j or i < len(l[1]):
                    f.write(l[0] + ', ')
            f.write('\n')


def get_resource_owners(filename: str, resources_name: str) -> list:
    with open(filename, 'r') as f:
        for line in f:
            if resources_name in line:
                return line.replace('\n', '').split('\t')[1].split(',')[:-1]


def get_user_resources(filename: str, user_name: str) -> list:
    resources = []
    with open(filename, 'r') as f:
        for line in f:
            if user_name in line:
                resources.append(line.replace('\n', '').split('\t')[0])
    return resources


if __name__ == '__main__':
    hierarchy = Hierarchy()
    hierarchy.init_from_file('hierarchy.txt')
    generate_resources_rights(hierarchy.hierarchy, 'resources.txt')
    print(get_resource_owners('resources.txt', 'John Smith'))
    print(get_user_resources('users.txt', 'John Smith'))
