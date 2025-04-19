import numpy as np
from typing import Union, Collection, List

class _ArrayVisuliserElement(object):

    def __init__(self, title: Union[str, None], data: np.ndarray):
        self.__title = title if title is not None else ""
        self.__data = np.array(data)
        self.__dimensions = len(self.__data.shape)
        self.__count = np.prod(self.__data.shape)
        self.__minimal_count_string = f"{self.__count}" + ("" if self.__dimensions == 1 else f" ({', '.join([str(v) for v in self.__data.shape])})")

        self.__required_title_characters = len(self.__title)
        self.__min_required_count_characters = int(np.log10(self.__count)) + 1 + (0 if self.__dimensions == 1 else (3 + sum(int(np.log10(l)) + 1 for l in self.__data.shape) + (2 * (self.__dimensions - 1))))
        self.__max_count_characters_total_count = int(np.log10(self.__count)) + 1
        self.__max_count_characters_per_dimension = [int(np.log10(dimension_size)) + 1 for dimension_size in self.__data.shape]

        self.__percent = lambda n: 100 * n / self.__count

        self.__n_nan                      = np.isnan(  self.__data                                       )
        self.__n_negitive_inf             =         (  self.__data == -np.inf                            )
        self.__n_positive_inf             =         (  self.__data ==  np.inf                            )
        self.__n_negitive                 =         ( (self.__data  <  0)     & (self.__data != -np.inf) )
        self.__n_zero                     =         (  self.__data ==  0                                 )
        self.__n_positive                 =         ( (self.__data  >  0)     & (self.__data !=  np.inf) )
        self.__n_negitive_1_to_below_zero =         ( (self.__data >= -1)     & (self.__data <  0)       )
        self.__n_above_zero_to_positive_1 =         ( (self.__data <=  1)     & (self.__data >  0)       )
        self.__n_negitive_e_to_below_zero =         ( (self.__data >= -np.e)  & (self.__data <  0)       )
        self.__n_above_zero_to_positive_e =         ( (self.__data <=  np.e)  & (self.__data >  0)       )

        if self.__dimensions == 1:
            self.__n_nan                      = self.__n_nan.sum()
            self.__n_negitive_inf             = self.__n_negitive_inf.sum()
            self.__n_positive_inf             = self.__n_positive_inf.sum()
            self.__n_negitive                 = self.__n_negitive.sum()
            self.__n_zero                     = self.__n_zero.sum()
            self.__n_positive                 = self.__n_positive.sum()
            self.__n_negitive_1_to_below_zero = self.__n_negitive_1_to_below_zero.sum()
            self.__n_above_zero_to_positive_1 = self.__n_above_zero_to_positive_1.sum()
            self.__n_negitive_e_to_below_zero = self.__n_negitive_e_to_below_zero.sum()
            self.__n_above_zero_to_positive_e = self.__n_above_zero_to_positive_e.sum()
        else:
            axes = np.array(np.arange(self.__dimensions), dtype = int)
            summation_axis_tuples = [
                tuple(axes[axes != axis_index])
                for axis_index
                in axes
            ]

            self.__n_nan                      = (self.__n_nan.sum(),                      [(self.__n_nan.sum(                      axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_negitive_inf             = (self.__n_negitive_inf.sum(),             [(self.__n_negitive_inf.sum(             axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_positive_inf             = (self.__n_positive_inf.sum(),             [(self.__n_positive_inf.sum(             axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_negitive                 = (self.__n_negitive.sum(),                 [(self.__n_negitive.sum(                 axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_zero                     = (self.__n_zero.sum(),                     [(self.__n_zero.sum(                     axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_positive                 = (self.__n_positive.sum(),                 [(self.__n_positive.sum(                 axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_negitive_1_to_below_zero = (self.__n_negitive_1_to_below_zero.sum(), [(self.__n_negitive_1_to_below_zero.sum( axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_above_zero_to_positive_1 = (self.__n_above_zero_to_positive_1.sum(), [(self.__n_above_zero_to_positive_1.sum( axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_negitive_e_to_below_zero = (self.__n_negitive_e_to_below_zero.sum(), [(self.__n_negitive_e_to_below_zero.sum( axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
            self.__n_above_zero_to_positive_e = (self.__n_above_zero_to_positive_e.sum(), [(self.__n_above_zero_to_positive_e.sum( axis = summation_axis_tuples[i]) > 0).sum() for i in range(len(summation_axis_tuples))])
        
        self.__minimum_non_infinate_value =                                                                             self.__data[(self.__data != -np.inf) & (~np.isnan(self.__data))                     ].min() if ((self.__data != -np.inf) & (~np.isnan(self.__data))).sum() > 0 else None
        self.__maximum_non_infinate_value =                                                                             self.__data[(self.__data !=  np.inf) & (~np.isnan(self.__data))                     ].max() if ((self.__data !=  np.inf) & (~np.isnan(self.__data))).sum() > 0 else None
        self.__smallest_nonzero_value     = self.__data[(self.__data != 0) & (~np.isnan(self.__data))].flatten()[np.abs(self.__data[(self.__data !=  0)      & (~np.isnan(self.__data))].flatten()).argmin()]       if ((self.__data !=  0     ) & (~np.isnan(self.__data))).sum() > 0 else None

    @property
    def _required_title_characters(self):
        return self.__required_title_characters
    @property
    def _min_required_count_characters(self):
        return self.__min_required_count_characters

    def __str__(self):
        return f"{self.__title} | {self.__minimal_count_string}"

    def render_title(self, line_length: int, internal: bool) -> str:
        sep = "-" if internal else ","

        if self.__title.strip() != "":
            n_extra_dashes = line_length - 6 - len(self.__title)
            n_dashes_left =  int(n_extra_dashes / 2)
            n_dashes_right =  (int(n_extra_dashes / 2) + (0 if n_extra_dashes % 2 == 0 else 1))
            return f"{sep * (n_dashes_left + 2)} {self.__title} {sep * (n_dashes_right + 2)}"

        else:
            return sep * line_length

    def render_body(self, max_count_char_allowence: int, line_length: int, show_plus_minus_1: bool, show_plus_minus_e: bool, show_min_max: bool, max_unused_decimal_places_for_minmax: int) -> str:
        row_padding = " " * _ArrayVisuliserElement._calculate_row_padding(max_count_char_allowence, line_length)

        multi_dimensional_count_format_insert = None
        if self.__dimensions > 1:
            multi_dimensional_count_format_insert = (" " * (max_count_char_allowence - self.__min_required_count_characters)) + f"{{:{self.__max_count_characters_total_count}.0f}}" + " (" + ", ".join([f"{{:{self.__max_count_characters_per_dimension[i]}.0f}}" for i in range(self.__dimensions)]) + ")"

        lines = []

        # Number
        lines.append(
            f"    N    :         : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__count)
            if self.__dimensions == 1 else
            f"    N    :         : {' ' * (max_count_char_allowence - self.__min_required_count_characters)}{self.__minimal_count_string} {row_padding}"
        )

        # +inf
        lines.append(
            f"    \u221E    : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_positive_inf), self.__n_positive_inf)
            if self.__dimensions == 1 else
            f"    \u221E    : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_positive_inf[0]), self.__n_positive_inf[0], *self.__n_positive_inf[1])
        )

        # Positive
        lines.append(
            f"   +ve   : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_positive), self.__n_positive)
            if self.__dimensions == 1 else
            f"   +ve   : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_positive[0]), self.__n_positive[0], *self.__n_positive[1])
        )

        # Zero
        lines.append(
            f"    0    : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_zero), self.__n_zero)
            if self.__dimensions == 1 else
            f"    0    : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_zero[0]), self.__n_zero[0], *self.__n_zero[1])
        )

        # Negitive
        lines.append(
            f"   -ve   : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_negitive), self.__n_negitive)
            if self.__dimensions == 1 else
            f"   -ve   : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_negitive[0]), self.__n_negitive[0], *self.__n_negitive[1])
        )

        # -inf
        lines.append(
            f"   -\u221E    : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_negitive_inf), self.__n_negitive_inf)
            if self.__dimensions == 1 else
            f"   -\u221E    : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_negitive_inf[0]), self.__n_negitive_inf[0], *self.__n_negitive_inf[1])
        )

        # NaN
        lines.append(
            f"   nan   : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_nan), self.__n_nan)
            if self.__dimensions == 1 else
            f"   nan   : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_nan[0]), self.__n_nan[0], *self.__n_nan[1])
        )

        if show_plus_minus_1:
        
            # Blank line to seperate sections
            lines.append(
                f"         :         : {' ' * max_count_char_allowence} {row_padding}"
            )

            # 1 >= v > 0
            lines.append(
                f" +1\u2265x> 0 : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_above_zero_to_positive_1), self.__n_above_zero_to_positive_1)
                if self.__dimensions == 1 else
                f" +1\u2265x> 0 : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_above_zero_to_positive_1[0]), self.__n_above_zero_to_positive_1[0], *self.__n_above_zero_to_positive_1[1])
            )

            # 0 > v >= -1
            lines.append(
                f"  0>x\u2265-1 : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_negitive_1_to_below_zero), self.__n_negitive_1_to_below_zero)
                if self.__dimensions == 1 else
                f"  0>x\u2265-1 : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_negitive_1_to_below_zero[0]), self.__n_negitive_1_to_below_zero[0], *self.__n_negitive_1_to_below_zero[1])
            )

        if show_plus_minus_e:
        
            # Blank line to seperate sections
            lines.append(
                f"         :         : {' ' * max_count_char_allowence} {row_padding}"
            )

            # 1 >= v > 0
            lines.append(
                f" +e\u2265x> 0 : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_above_zero_to_positive_e), self.__n_above_zero_to_positive_e)
                if self.__dimensions == 1 else
                f" +e\u2265x> 0 : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_above_zero_to_positive_e[0]), self.__n_above_zero_to_positive_e[0], *self.__n_above_zero_to_positive_e[1])
            )

            # 0 > v >= -1
            lines.append(
                f"  0>x\u2265-e : {{:6.2f}}% : {{:{max_count_char_allowence}.0f}} {row_padding}".format(self.__percent(self.__n_negitive_e_to_below_zero), self.__n_negitive_e_to_below_zero)
                if self.__dimensions == 1 else
                f"  0>x\u2265-e : {{:6.2f}}% : {multi_dimensional_count_format_insert} {row_padding}".format(self.__percent(self.__n_negitive_e_to_below_zero[0]), self.__n_negitive_e_to_below_zero[0], *self.__n_negitive_e_to_below_zero[1])
            )

        if show_min_max:
            
            if self.__maximum_non_infinate_value is None and self.__smallest_nonzero_value is None and self.__minimum_non_infinate_value is None:
                fmt = "{}"
            else:
                max_chars = max_count_char_allowence + 10
                n_chars_for_int_portion = max(1, 1 + int( np.log10(max(np.abs(self.__maximum_non_infinate_value) if (self.__maximum_non_infinate_value is not None and self.__maximum_non_infinate_value != 0) else 1, np.abs(self.__smallest_nonzero_value) if (self.__smallest_nonzero_value is not None and self.__smallest_nonzero_value != 0) else 1, np.abs(self.__minimum_non_infinate_value) if (self.__minimum_non_infinate_value is not None and self.__minimum_non_infinate_value != 0) else 1))))
                min_dp_for_precision    =        1 + int(-np.log10(min(np.abs(self.__maximum_non_infinate_value) if (self.__maximum_non_infinate_value is not None and self.__maximum_non_infinate_value != 0) else 1, np.abs(self.__smallest_nonzero_value) if (self.__smallest_nonzero_value is not None and self.__smallest_nonzero_value != 0) else 1, np.abs(self.__minimum_non_infinate_value) if (self.__minimum_non_infinate_value is not None and self.__minimum_non_infinate_value != 0) else 1)))
                n_dp = max(min(max_unused_decimal_places_for_minmax, max_chars - n_chars_for_int_portion - 1), min_dp_for_precision)
                fmt = f"{{:{max_chars}.{n_dp}f}}"
        
            # Blank line to seperate sections
            lines.append(
                f"         :         : {' ' * max_count_char_allowence} {row_padding}"
            )

            # 1 >= v > 0
            insert_value = fmt.format(self.__maximum_non_infinate_value)
            lines.append(
                f"max   \u2260 \u221E: {' ' * (max_count_char_allowence - len(insert_value) + 10)}{insert_value} {row_padding}"
                if self.__maximum_non_infinate_value is not None else
                f"max   \u2260 \u221E: N/A       {' ' * max_count_char_allowence} {row_padding}"
            )

            # 1 >= v > 0
            insert_value = fmt.format(self.__smallest_nonzero_value)
            lines.append(
                f"small \u2260 0: {' ' * (max_count_char_allowence - len(insert_value) + 10)}{insert_value} {row_padding}"
                if self.__smallest_nonzero_value is not None else
                f"small \u2260 0: N/A       {' ' * max_count_char_allowence} {row_padding}"
            )

            # 0 > v >= -1
            insert_value = fmt.format(self.__minimum_non_infinate_value)
            lines.append(
                f"min   \u2260-\u221E: {' ' * (max_count_char_allowence - len(insert_value) + 10)}{insert_value} {row_padding}"
                if self.__minimum_non_infinate_value is not None else
                f"min   \u2260-\u221E: N/A       {' ' * max_count_char_allowence} {row_padding}"
            )

        # Blank line at bottom
        lines.append(
            f"         :         : {' ' * max_count_char_allowence} {row_padding}"
        )

        return "\n".join(lines)

    @staticmethod
    def render_bottom(line_length: int) -> str:
        return "-" * line_length

    @staticmethod
    def render_empty_title(line_length: int) -> str:
        return " " * line_length

    @staticmethod
    def render_empty_body(line_length: int, show_plus_minus_1: bool, show_plus_minus_e: bool, show_min_max: bool) -> str:
        return "\n".join([" " * line_length] * (8 + (3 if show_plus_minus_1 else 0) + (3 if show_plus_minus_e else 0) + (4 if show_min_max else 0)))
    
    @staticmethod
    def get_smallest_body_line_length():
        return 22 + 1

    @staticmethod
    def calculate_min_line_length(max_title_char_allowence: int, max_count_char_allowence: int):
        return max(6 + max_title_char_allowence, 22 + max_count_char_allowence)

    @staticmethod
    def _calculate_row_padding(max_count_char_allowence: int, line_length: int):
        return max(0, line_length - (22 + max_count_char_allowence))

class ArrayVisuliser(object):

    def __init__(self,
                 datasets: Union[np.ndarray, Collection[Union[np.ndarray, None]], Collection[Collection[Union[np.ndarray, None]]]],
                 titles: Union[str, Collection[Union[str, None]], Collection[Collection[Union[str, None]]], None] = None,
                 number_missing_titles = True):

        # Is there just one dataset?
        if not isinstance(datasets, list):
            datasets = [[datasets]]
            if titles is not None:
                titles = [[titles]]

        # Is there just one row of datasets?
        elif not isinstance(datasets[0], list):
            datasets = [datasets]
            if titles is not None:
                titles = [titles]

        self.__n_width = len(datasets[0])
        self.__n_height = len(datasets)
        self.__elements: List[List[Union[_ArrayVisuliserElement, None]]] = [
            [
                (_ArrayVisuliserElement(titles[row][col] if titles is not None else (f"(#{row * self.__n_width + col})" if number_missing_titles else None),
                                       datasets[row][col])
                if datasets[row][col] is not None else
                None)
                for col
                in range(self.__n_width)
            ]
            for row
            in range(self.__n_height)
        ]

        self.__number_of_elements = self.__n_width * self.__n_height

        self.__count = sum([
                                sum([
                                        1 if self.__elements[i][j] is not None else 0
                                        for j
                                        in range(self.__n_width)
                                ])
                                for i
                                in range(self.__n_height)
                       ])

    def __len__(self):
        return self.__count
    
    @property
    def number_of_cells(self):
        return self.__number_of_elements

    def __str__(self):
        return "\n".join(["\n".join([element.__str__() for element in row]) for row in self.__elements])

    def render(self, all_columns_same_width = False, min_count_allowence: int = 0, show_plus_minus_1: bool = False, show_plus_minus_e: bool = False, show_min_max: bool = True, max_unused_decimal_places_for_minmax: int = 3):
        result = None

        column_count_chars = [
            max(max([
                    (self.__elements[row][col]._min_required_count_characters
                    if self.__elements[row][col] is not None else
                    1)
                    for row
                    in range(self.__n_height)
                ]),
                min_count_allowence)
            for col
            in range(self.__n_width)
        ]

        column_line_lengths = [
            max([
                (_ArrayVisuliserElement.calculate_min_line_length(self.__elements[row][col]._required_title_characters, column_count_chars[col])
                if self.__elements[row][col] is not None else
                _ArrayVisuliserElement.get_smallest_body_line_length())
                for row
                in range(self.__n_height)
            ])
            for col
            in range(self.__n_width)
        ]
        if all_columns_same_width:
            column_line_lengths = [max(column_line_lengths)] * len(column_line_lengths)

        row_strings = []
        for row in range(self.__n_height):
            is_top_row = row == 0
            is_bottom_row = row == self.__n_height - 1

            rendered_element_lines = []
            for col in range(self.__n_width):
                rendered_element_lines.append((self.__elements[row][col].render_body(column_count_chars[col], column_line_lengths[col], show_plus_minus_1, show_plus_minus_e, show_min_max, max_unused_decimal_places_for_minmax) if self.__elements[row][col] is not None else _ArrayVisuliserElement.render_empty_body(column_line_lengths[col], show_plus_minus_1, show_plus_minus_e, show_min_max)).split("\n"))

            total_lines_per_render = len(rendered_element_lines[0])

            row_lines = [""] * (total_lines_per_render + (1 if not is_bottom_row else 2))
            for col in range(self.__n_width):
                is_populated_dataset = self.__elements[row][col] is not None
#                is_dataset_to_left = col > 0 and self.__elements[row][col - 1] is not None
                is_dataset_to_right = col < self.__n_width - 1 and self.__elements[row][col + 1] is not None
                is_dataset_above = not is_top_row and self.__elements[row - 1][col] is not None
#                is_dataset_below = not is_bottom_row and self.__elements[row + 1][col] is not None
                is_dataset_diagonal_above_and_right = not is_top_row and col < self.__n_width - 1 and self.__elements[row - 1][col + 1] is not None

                if col == 0:
                    row_lines[0] += "#" if is_populated_dataset or is_dataset_above else " "
                row_lines[0] += self.__elements[row][col].render_title(column_line_lengths[col], not is_dataset_above) if is_populated_dataset else _ArrayVisuliserElement.render_bottom(column_line_lengths[col]) if is_dataset_above else _ArrayVisuliserElement.render_empty_title(column_line_lengths[col])
                row_lines[0] += "#" if is_populated_dataset or is_dataset_to_right or is_dataset_above or is_dataset_diagonal_above_and_right else " "

                for i in range(total_lines_per_render):
                    if col == 0:
                        row_lines[i + 1] += "|" if is_populated_dataset else " "
                    row_lines[i + 1] += rendered_element_lines[col][i]
                    row_lines[i + 1] += ("¦" if is_populated_dataset else "|") if is_dataset_to_right else ("|" if is_populated_dataset else " ")

                if is_bottom_row:
                    if col == 0:
                        row_lines[-1] += "#" if is_populated_dataset else " "
                    row_lines[-1] += _ArrayVisuliserElement.render_bottom(column_line_lengths[col]) if is_populated_dataset else _ArrayVisuliserElement.render_empty_title(column_line_lengths[col])
                    row_lines[-1] += "#" if is_populated_dataset or is_dataset_to_right else " "

            row_strings.append("\n".join(row_lines))

        result = "\n".join(row_strings)

        return result

    def print(self, *args, all_columns_same_width = False, min_count_allowence: int = 0, show_plus_minus_1: bool = False, show_plus_minus_e: bool = False, show_min_max: bool = True, **kwargs):
        print(self.render(all_columns_same_width = all_columns_same_width,
                          min_count_allowence = min_count_allowence,
                          show_plus_minus_1 = show_plus_minus_1,
                          show_plus_minus_e = show_plus_minus_e,
                          show_min_max = show_min_max),
              *args,
              **kwargs)

    @staticmethod
    def arrange(columns: int, datasets: Collection[np.ndarray], titles: Union[List[Union[str, None]], None] = None):
        if not isinstance(columns, int):
            raise TypeError(f"Number of columns must be an integer not {type(columns)}")
        if columns < 1:
            raise ValueError(f"Number of columns must be nonzero and positive but was {columns}")
        if not isinstance(datasets, Collection):
            raise TypeError("More than one dataset must be passed.")
        if titles is not None and len(datasets) != len(titles):
            raise ValueError("Mismatched number of datasets and titles.")

        n_datasets = len(datasets)
        n_rows = int(n_datasets / columns) + (0 if n_datasets % columns == 0 else 1)

        return ArrayVisuliser([[(datasets[i * columns + j] if (i * columns + j < n_datasets) else None) for j in range(columns)] for i in range(n_rows)],
                              [[(  titles[i * columns + j] if (i * columns + j < n_datasets) else None) for j in range(columns)] for i in range(n_rows)] if titles is not None else None)

    @staticmethod
    def row(*datasets: np.ndarray, titles: Union[List[Union[str, None]], None] = None):
        if len(datasets) == 0:
            raise TypeError("More than one dataset must be passed.")
        if titles is not None and len(datasets) != len(titles):
            raise ValueError("Mismatched number of datasets and titles.")
        return ArrayVisuliser(datasets = [datasets], titles = [titles] if titles is not None else None)

    @staticmethod
    def column(*datasets: np.ndarray, titles: Union[List[Union[str, None]], None] = None):
        if len(datasets) == 0:
            raise TypeError("More than one dataset must be passed.")
        if titles is not None and len(datasets) != len(titles):
            raise ValueError("Mismatched number of datasets and titles.")
        return ArrayVisuliser(datasets = [[d] for d in datasets],
                              titles = [[t] for t in titles] if titles is not None else None)
