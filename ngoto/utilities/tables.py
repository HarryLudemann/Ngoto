# script contains class to create tables from dynamic information eg.

# +------------+------------+
# | column 1   | column 2   |
# +============+============+
# | value1     | value2     |
# +------------+------------+
# | value3     | value4     |
# +------------+------------+

class Table():
    col_widths = []
    def set_col_widths(self, col_widths):
        self.col_widths = col_widths

    def get_sep(self, width, char):
        """ given int width, and string char of character"""
        seperator = ''
        for _ in range(width):
            seperator += char
        return seperator

    def value_check(self, value, max):
        if len(value) > max:
            value = value[:max-4]
            value += '..'
        return value

    def first_row_value(self, value, width):
        value = self.value_check(value, width)
        row_padding = width - len(value)
        text = ' ' + value + self.get_sep(row_padding - 1, ' ')
        seperator = '+' + self.get_sep(width, '-') + '+'
        return f'|{text}|\n{seperator}'

    def row_item_value(self, value, width):
        value = self.value_check(value, width)
        row_padding = width - len(value)
        text = ' ' + value + self.get_sep(row_padding - 1, ' ')
        seperator = self.get_sep(width, '-') + '+'
        return f'{text}|\n{seperator}'

    def get_table_row(self, values, col_widths):
        """ Given list of column names and list of values. prints table
        doesnt return """
        first_value = self.first_row_value(values[0], col_widths[0]) # First value
        values.pop(0) # remove first value from list
        result = '' # final table string
        table_titles = [] # list of formatted column tables
        for index, name in enumerate(values):
            table_titles.append(self.row_item_value(name, col_widths[index + 1]))
        # merging muilti line strings side by side
        for index, line in enumerate(iter( first_value.splitlines() )):
            full_line = line
            for table in table_titles:
                full_line += table.splitlines()[index]
            result += full_line + '\n'
        return result

    def get_table(self, col_names, col_widths, col_values):
        """given list of names and list of lists of values"""
        self.col_widths = col_widths
        result = self.get_table_row(col_names, col_widths)
        for values in col_values:
            result += self.get_table_row(values, col_widths)
        return result

    

if __name__ == '__main__':
    col_widths = [5, 10, 10]
    col_names = ['Test', 'Testing', 'Testin']
    col_values = [
        ['1124124', '2352', '253'],
        ['45325253', '553', '36'],
        ['7', '853', '25asasasd259']
    ]
    
    # tb = Table()
    # tb.set_col_widths(col_widths)
    # result = tb.get_table_row(col_names)
    # for values in col_values:
    #     result += tb.get_table_row(values)

    print( '\n' + Table().get_table(col_names, col_widths, col_values) )
    