class FirmHistory:
    def __init__(self, name, step_count):
        self.title = name
        self.salaries = [0] * step_count
        self.prices = [0] * step_count
        self.workers_counts = [0] * step_count
        self.sales = [0] * step_count
        self.storage = [0] * step_count
        self.profits = [0] * step_count
        self.money = [0] * step_count
        self.sold = [0] * step_count

    def add_record(self, step, firm):
        self.salaries[step] = firm.salary
        self.prices[step] = firm.price
        self.workers_counts[step] = len(firm.workers)
        self.sales[step] = firm.sales
        self.storage[step] = firm.stock
        self.profits[step] = firm.profit
        self.money[step] = firm.money
        self.sold[step] = firm.sold
