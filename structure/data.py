import experiments, measurements, infos, data
import machines

class Data():
    def __init__(self):
        print('NEW\t Data')

    def import_data(self, machine, file):
        machines = {'SushiBar': machines.SushiBar()}

        self.__raw_data = machines[machine(file)]

class Data2D(Data):
    pass