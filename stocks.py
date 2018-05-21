class Logistics:
    def __init__(self):
        pass

    def grahams(self, timeseries, amount):
        days = 1
        total = 0;
        for tt in timeseries:
            total = total + round(float(tt['4. close']), 2)
            days = days + 1

        eps = total / days
        g = 5  # projected for 10 years

        no_of_shares = amount / eps;

        pr = eps * (8.5 + g) / 10

        return pr * no_of_shares

    def graph(self, data, total_history):
        graph = {}
        j = 0

        for data_key in data.keys():

            if (j > 10):
                break

            graph[data_key] = float(data[data_key]['4. close'])

            if data_key in total_history:
                total_history[data_key] += round(float(data[data_key]['4. close']), 2)
            else:
                total_history[data_key] = round(float(data[data_key]['4. close']), 2);

            j += 1

        return graph


class Options:
    GROWTH_STOCK = ['NFLX', 'INTC', 'CSCO']
    INDEX_STOCK = ['DJIA', 'DJU', 'SPX']
    VALUE_STOCK = ['GM', 'STX', 'BBY']
    ETHICAL_STOCK = ['AAPL', 'ADBE', 'NSRGY']
    QUALITY_STOCK = ['SPHQ', 'DGRW', 'QDF']

    def __init__(self, options):
        self.options = options

    def fetch(self):
        stock_info = []
        str_header = ''

        if 'Growth Investing' in self.options:
            stock_info += Options.GROWTH_STOCK
            if str_header != '':
                str_header += 'and '

            str_header += ' Growth Investing '

        if 'Index Investing' in self.options:
            stock_info += Options.INDEX_STOCK
            if str_header != '':
                str_header += 'and '

            str_header += 'Index Investing '

        if 'Value Investing' in self.options:
            stock_info += Options.VALUE_STOCK
            if str_header != '':
                str_header += 'and '

            str_header += 'Value Investing '

        if 'Ethical Investing' in self.options:
            stock_info += Options.ETHICAL_STOCK
            if str_header != '':
                str_header += 'and '

            str_header += 'Ethical Investing '

        if 'Quality Investing' in self.options:
            stock_info += Options.QUALITY_STOCK
            if str_header != '':
                str_header += 'and '

            str_header += 'Quality Investing'

        return stock_info, str_header


def roundSet(number_set):
    unround_numbers = [x / float(sum(number_set)) * 100 * 10 for x in number_set]
    decimal_part_with_index = sorted([(index, unround_numbers[index] % 1) for index in range(len(unround_numbers))],
                                     key=lambda y: y[1], reverse=True)
    remainder = 100 * 10 - sum([int(x) for x in unround_numbers])
    index = 0
    while remainder > 0:
        unround_numbers[decimal_part_with_index[index][0]] += 1
        remainder -= 1
        index = (index + 1) % len(number_set)
    return [int(x) / 10 for x in unround_numbers]
