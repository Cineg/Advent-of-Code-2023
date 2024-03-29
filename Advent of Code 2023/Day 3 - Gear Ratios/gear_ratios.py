from dataclasses import dataclass
from input import INPUT


@dataclass
class SchematicNumber:
    row: int
    start_index: int
    end_index: int
    number: int

    min_row: int = 0
    max_row: int = 0
    min_col: int = 0
    max_col: int = 0

    star_location: tuple[int, int] | None = None

    def is_special_character_adjacent(self, data: list[str]) -> bool:
        self._get_boundaries(len(data), len(data[0]))

        for row in range(self.min_row, self.max_row):
            for col in range(self.min_col, self.max_col):
                if not data[row][col].isnumeric() and data[row][col] != ".":
                    return True

        return False

    def is_multiplier_adjacent(self, data: list[str]) -> bool:
        self._get_boundaries(len(data), len(data[0]))

        for row in range(self.min_row, self.max_row):
            for col in range(self.min_col, self.max_col):
                if data[row][col] == "*":
                    self.star_location = row, col
                    return True

        return False

    def _get_boundaries(self, last_data_row: int, last_data_column: int) -> None:
        if self.row == 0:
            self.min_row = 0
        else:
            self.min_row = self.row - 1

        if self.start_index == 0:
            self.min_col = 0
        else:
            self.min_col = self.start_index - 1

        if self.row + 1 == last_data_row:
            self.max_row = last_data_row
        else:
            self.max_row = self.row + 2

        if self.end_index + 1 == last_data_column:
            self.max_col = last_data_column
        else:
            self.max_col = self.end_index + 2


def main() -> None:
    data: list[str] = INPUT.splitlines()
    schematics: list[SchematicNumber] = _get_numbers_coordinates(data)
    schematics_multipliers: list[SchematicNumber] = []
    total: int = 0
    gears_total: int = 0

    used_indexes: dict = {}

    for item in schematics:
        if item.is_special_character_adjacent(data):
            total += item.number
        if item.is_multiplier_adjacent(data):
            schematics_multipliers.append(item)

    left_pointer: int = 0
    while left_pointer + 1 <= len(schematics_multipliers):
        for right_pointer in range(left_pointer + 1, len(schematics_multipliers)):
            if (
                schematics_multipliers[left_pointer].star_location
                == schematics_multipliers[right_pointer].star_location
            ):
                if left_pointer in used_indexes or right_pointer in used_indexes:
                    pass
                else:
                    gears_total += (
                        schematics_multipliers[left_pointer].number
                        * schematics_multipliers[right_pointer].number
                    )
                    used_indexes[left_pointer] = left_pointer
                    used_indexes[right_pointer] = right_pointer

        left_pointer += 1

    print(total)
    print(gears_total)


def _get_numbers_coordinates(data: list[str]) -> list[SchematicNumber]:
    start_index: int | None = None
    end_index: int | None = None
    number: str = ""
    nums: list[SchematicNumber] = []
    for row, line in enumerate(data):
        for column, character in enumerate(line):
            if character.isnumeric():
                if start_index == None:
                    start_index = column
                end_index = column
                number += character

            if not character.isnumeric():
                if start_index != None:
                    schematic_number: SchematicNumber = SchematicNumber(
                        row,
                        start_index=start_index,
                        end_index=end_index,
                        number=int(number),
                    )
                    nums.append(schematic_number)

                    start_index = None
                    end_index = None
                    number = ""

    return nums


if __name__ == "__main__":
    main()
