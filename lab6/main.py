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
        self.sort()
        with open(filename, 'w') as f:
            for i in self.hierarchy:
                f.write('\t' * (len(i[1]) - 1) + i[0] + '\n')

    def add_user(self, user_name: str, place: list):
        if place not in self.hierarchy.values():
            self.hierarchy[user_name] = place.copy()
        else:
            raise Exception(f'Cant add user {user_name} on this {place=}')

    def remove_user(self, user_name: str):
        if user_name in self.hierarchy:
            del self.hierarchy[user_name]
        else:
            raise Exception(f'Cant remove user {user_name}, that user does not exist')

    def sort(self):
        self.hierarchy.sort(key=lambda x: x.place)

    def get_user_place(self, user_name: str) -> list:
        if user_name in self.hierarchy:
            return self.hierarchy[user_name]
        else:
            raise Exception(f'Cant get user {user_name}, that user does not exist')

    def get_user_by_place(self, place: list) -> list:
        if place in self.hierarchy.values():
            for user, _place in self.hierarchy.items():
                if _place == place:
                    return user
        else:
            raise Exception(f'Cant get user {place}, that place does not exist')

    def generate_resources_rights(self, filename: str):
        resources = []
        with open(filename, 'r') as f:
            for line in f:
                resources.append(line.replace('\n', ''))
        with open(str(filename.split('.')[0] + '&rights.txt'), 'w') as f:
            for res in resources:
                all_owners = set()
                owners = res.split('\t')[1].split(',')[:-1]  # find final owners
                res = res.split('\t')[0]
                if 'price.xlsx' in res:
                    pass
                for owner in owners:
                    all_owners.add(owner)
                    place = (self.hierarchy[owner])
                    for i in range(len(place)):
                        upper_user_place = place[:-i]
                        if upper_user_place in self.hierarchy.values():
                            upper_user = self.get_user_by_place(upper_user_place)
                            all_owners.add(upper_user)
                f.write(res + '\t')
                for owner in all_owners:
                    f.write(owner + ',')
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
    hierarchy.generate_resources_rights('res1.txt')
    '''
    print(get_resource_owners('res1&rights.txt', 'John Smith'))
    print(get_user_resources('res1&rights.txt', 'John Smith'))

    try:
        hierarchy.add_user('Lisa Yen', [0, 1, 4])
        hierarchy.add_user('John Done', [0])
    except Exception as e:
        print(e)

    print(hierarchy.hierarchy)

    try:
        hierarchy.remove_user('Lisa Yen')
        hierarchy.remove_user('John Done')
    except Exception as e:
        print(e)

    print(hierarchy.hierarchy)
 '''
