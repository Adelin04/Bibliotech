_List = []


class AutoIncrement():

    def __init__(self, start_id, file):
        self.id = start_id
        self.file = file

    def read_file(file_name):
        with open(str(file_name) + '.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line == '':
                    continue

                data_product = line.split(',')

                _List.append({
                    'id': data_product[0],
                })

        #print(_List)
        return _List

    def next_id(self):
        _List.clear()
        AutoIncrement.read_file(self.file)
        if len(_List) == 0:
            return self.id
        else:
            _List.clear()
            AutoIncrement.read_file(self.file)
            for dic in _List:
                nextId = dic['id']
            self.id = int(nextId) + 1
            return self.id

    def Get_ID(self):
        return self.id