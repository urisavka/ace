from abc import ABCMeta

import algorithms

from history import History
from worker import Worker
from stats import Stats
from firm_action import FirmAction



class World:
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.firms = []
        self.workers = []

        self.stats = Stats()

        self.money = config['global']['initial_money']
        self.steps = config['global']['steps']

        self.firm_algorithms = config['algorithms']
        workers_count = config['global']['workers_count']
        self.config = config
        firm_counter = 0
        for class_, count in self.firm_algorithms.items():
            for i in range(int(count)):
                firm_class = getattr(algorithms, class_)
                firm = firm_class(firm_counter)
                self.firms.append(firm)
                firm_counter += 1
        firm_count = firm_counter
        # initial worker distribution
        for i in range(workers_count):
            worker = Worker(i)
            self.workers.append(worker)
            firm_id = i % firm_count
            firm = self.firms[firm_id]
            firm.add_worker(worker, firm.current_salary)

        self.history = History(self.steps, self.firms)

        self.firm_actions = [0] * firm_count
        self.firm_results = [0] * firm_count

    def manage_firm_actions(self, firm_actions):
        pass

    def compute_stats(self):
        self.stats.price = 0
        self.stats.stock = 0
        self.stats.sales = 0
        self.stats.sold = 0
        self.stats.salary = 0
        employed = 0
        for firm in self.firms:
            self.stats.price += firm.price
            self.stats.stock += firm.stock
            self.stats.sold += firm.sold
            self.stats.sales += firm.sales
            employed += len(firm.workers)
            for worker in firm.workers:
                self.stats.salary += worker.salary
        if self.stats.sold > 0:
            self.stats.price /= self.stats.sold
        else:
            self.stats.price = 0
        if employed > 0:
            self.stats.salary /= employed
        else:
            self.stats.salary = 0
        unemployed = 0
        for worker in self.workers:
            if worker.employer is None:
                unemployed += 1
        if len(self.workers) > 0:
            self.stats.unemployment_rate = unemployed / len(self.workers)
        self.stats.money = self.money

    def go(self):
        print("It's alive!!")
        birth_rate = self.config['global']['birth_rate']
        money_growth = self.config['global']['money_growth']
        for i, firm in enumerate(self.firms):
            self.firm_actions[firm.id] = FirmAction(0, firm.salary, firm.efficiency_coefficient * len(firm.workers), firm.price, 0, 0, [])
        for step in range(self.steps):
            # print("Step:", step)
            self.compute_stats()
            for i, firm in enumerate(self.firms):
                # @todo: enable bankrupt
                # if firm.money < self.config['global']['bankrupt_rate']:
                #     firm.bankrupt()
                #     del self.firms[i]
                #     del self.firm_actions[i]
                #     continue
                # print(firm)
                firm.work()
                # print(firm)
                #self.firm_actions[firm.id].production_count = firm.stock
            for j in range(birth_rate):
                worker = Worker(len(self.workers))
                self.workers.append(worker)
            self.manage_firm_actions(self.firm_actions)
            for firm_id, firm_action in enumerate(self.firm_actions):
                firm = self.firms[firm_id]
                firm.apply_result(self.firm_results[firm_id])
                self.history.add_record(step, firm)
            self.history.add_stats(step, self.stats)  # needs to be rewritten with proper history object in mind
            for i, firm in enumerate(self.firms):
                self.firm_actions[firm.id] = firm.decide(self.stats)
            self.money += money_growth

        return self.history
