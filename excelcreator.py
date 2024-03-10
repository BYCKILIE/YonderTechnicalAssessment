import pandas


class ExcelCreator:
    __stop = False

    def __init__(self, data: list):
        if not data:
            self.__stop = True
            return

        self.data_frame = pandas.DataFrame(data)

    # adjusting the length of the columns to fit the all the text displayed
    def adjust_cols_to_strlen(self, writer):
        worksheet = writer.sheets['Sheet1']
        for idx, col in enumerate(self.data_frame):
            series = self.data_frame[col]
            max_len = max((
                series.astype(str).map(len).max(),
                len(str(series.name))
            )) + 1
            worksheet.set_column(idx, idx, max_len)

    # styling borders for a more readable excel file
    def adjust_borders_to_format(self, writer):
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        limit_no = self.data_frame.shape[0] + 1

        border_general = workbook.add_format({'border': 1})
        border_left_corners = workbook.add_format({'top': 1, 'bottom': 1, 'left': 1})
        border_right_corners = workbook.add_format({'top': 1, 'bottom': 1, 'right': 1})

        # assign the cells what type of borders will have
        columns_borders = {
            'id': border_general,
            'nume': border_left_corners,
            'prenume': border_right_corners,
            'categorie': border_general,
            'dataDeEmitere': border_left_corners,
            'dataDeExpirare': border_right_corners,
            'suspendat': border_general,
            'total': border_general
        }

        for header in self.data_frame.columns:
            col_letter = chr(ord('A') + self.data_frame.columns.get_loc(header))
            col_data_range = f'{col_letter}2:{col_letter}{limit_no}'

            if header in columns_borders:
                worksheet.conditional_format(col_data_range, {'type': 'no_blanks', 'format': columns_borders[header]})

    def create_file(self, filename: str):
        if self.__stop:
            return
        if len(filename) < 5:
            filename += '.xlsx'
        elif filename[len(filename) - 5: len(filename)] != '.xlsx':
            filename += '.xlsx'

        with pandas.ExcelWriter(filename, engine='xlsxwriter') as writer:
            self.data_frame.to_excel(writer, index=False, sheet_name='Sheet1')
            self.adjust_cols_to_strlen(writer)
            self.adjust_borders_to_format(writer)

    def fail(self):
        return self.__stop
