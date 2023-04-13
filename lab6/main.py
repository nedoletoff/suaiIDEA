class Hierarchy:
    def __init__(self, filename=None):
        self.resources_rights_file = None
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

    def generate_resources_rights(self, in_filename: str, out_filename: str):
        resources = []
        with open(in_filename, 'r') as f:
            for line in f:
                resources.append(line.replace('\n', ''))
        with open(out_filename, 'w') as f:
            for res in resources:
                all_owners = set()
                owners = res.split('\t')[1].split(',')[:-1]  # find final owners
                res = res.split('\t')[0]
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
        self.resources_rights_file = out_filename


class ResourcesOwners:
    def __init__(self, filename, hierarchy=None):
        self.filename = filename
        self.hierarchy = hierarchy

    def get_resource_owners(self, resources_name: str) -> list:
        with open(self.filename, 'r') as f:
            for line in f:
                if resources_name in line:
                    return line.replace('\n', '').split('\t')[1].split(',')[:-1]

    def get_user_resources(self, user_name: str) -> list:
        resources = []
        with open(self.filename, 'r') as f:
            for line in f:
                if user_name in line:
                    resources.append(line.replace('\n', '').split('\t')[0])
        return resources

    def remove_resource(self, resource_name: str):
        with open(self.filename, 'r') as f:
            for line in f:
                if resource_name in line:
                    f.write(line.replace(resource_name, ''))

    def add_user_to_resource(self, user_name: str, resource_name: str):
        with open(self.filename, 'a') as f:
            f.write(resource_name + '\t' + user_name + ',\n')
            self.hierarchy.generate_resources_rights(self.filename, self.filename)

    def remove_user_access(self, user_name: str, resource_name: str):
        with open(self.filename, 'r') as f:
            for line in f:
                if user_name in line and resource_name in line:
                    f.write(line.replace(user_name + ',', ''))


def work_circle():
    exit_flag = False
    while not exit_flag:
        print('1. Add user')
        print('2. Remove user')
        print('3. Add resource')
        print('4. Remove resource')
        print('5. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            user_name = input('Enter user name: ')
            place = input('Enter place: ').split(',')
            try:
                hierarchy.add_user(user_name, place)
            except Exception as e:
                print(e)
        elif choice == '2':
            user_name = input('Enter user name: ')
            try:
                hierarchy.remove_user(user_name)
            except Exception as e:
                print(e)
        elif choice == '3':
            resource_name = input('Enter resource name: ')
            try:
                hierarchy.add_user_to_resource(user_name, resource_name)
            except Exception as e:
                print(e)
        elif choice == '4':
            resource_name = input('Enter resource name: ')




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
