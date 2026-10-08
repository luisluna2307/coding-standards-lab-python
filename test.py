"""Student Grade Management System.

Allows creating students, adding and removing grades, and generating
a summary report with average, letter grade, pass/fail and honor roll.
"""

MIN_GRADE = 0.0
MAX_GRADE = 100.0
PASSING_AVERAGE = 60.0
HONOR_ROLL_AVERAGE = 90.0

# (minimum average, letter) ordered from highest to lowest.
LETTER_THRESHOLDS = (
    (90.0, "A"),
    (80.0, "B"),
    (70.0, "C"),
    (60.0, "D"),
)
FAILING_LETTER = "F"


class Student:
    """Represents a student and the grades they have obtained."""

    def __init__(self, student_id, name):
        """Create a student after validating that ID and name are not empty."""
        self.student_id = self._validate_text(student_id, "Student ID")
        self.name = self._validate_text(name, "Student name")
        self.grades = []

    @staticmethod
    def _validate_text(value, field_name):
        """Return the stripped text, or raise ValueError if it is empty."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty text.")
        return value.strip()

    @staticmethod
    def _validate_grade(grade):
        """Return the grade as float, or raise ValueError if it is invalid."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError(f"Grade '{grade}' is not numeric.")
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise ValueError(
                f"Grade {grade} is out of range ({MIN_GRADE}-{MAX_GRADE})."
            )
        return float(grade)

    def add_grade(self, grade):
        """Add a numeric grade between 0 and 100."""
        self.grades.append(self._validate_grade(grade))

    def remove_grade_by_value(self, grade):
        """Remove the first grade equal to the given value."""
        value = self._validate_grade(grade)
        if value not in self.grades:
            raise ValueError(f"Grade {value} does not exist.")
        self.grades.remove(value)

    def remove_grade_by_index(self, index):
        """Remove the grade at the given position (0-based)."""
        if not 0 <= index < len(self.grades):
            raise IndexError(
                f"Index {index} is out of bounds "
                f"(student has {len(self.grades)} grades)."
            )
        del self.grades[index]

    def calculate_average(self):
        """Return the average of all grades, or 0.0 if there are none."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def get_letter_grade(self):
        """Convert the average into a letter grade (A, B, C, D or F)."""
        average = self.calculate_average()
        for minimum, letter in LETTER_THRESHOLDS:
            if average >= minimum:
                return letter
        return FAILING_LETTER

    def has_passed(self):
        """Return True if the average is 60 or higher."""
        return self.calculate_average() >= PASSING_AVERAGE

    def is_on_honor_roll(self):
        """Return True if the average is 90 or higher."""
        return self.calculate_average() >= HONOR_ROLL_AVERAGE

    def generate_report(self):
        """Return a formatted summary report of the student."""
        status = "Passed" if self.has_passed() else "Failed"
        lines = [
            "=" * 35,
            "STUDENT SUMMARY REPORT",
            "=" * 35,
            f"Student ID      : {self.student_id}",
            f"Student Name    : {self.name}",
            f"Number of Grades: {len(self.grades)}",
            f"Average Grade   : {self.calculate_average():.2f}",
            f"Letter Grade    : {self.get_letter_grade()}",
            f"Pass/Fail       : {status}",
            f"Honor Roll      : {self.is_on_honor_roll()}",
            "=" * 35,
        ]
        return "\n".join(lines)


def create_student(student_id, name):
    """Create a student, showing an error message if the data is invalid."""
    try:
        return Student(student_id, name)
    except ValueError as error:
        print(f"Error: {error}")
        return None


def add_grade_safely(student, grade):
    """Add a grade, showing an error message if it is invalid."""
    try:
        student.add_grade(grade)
    except ValueError as error:
        print(f"Error: {error}")


def remove_by_value_safely(student, grade):
    """Remove a grade by value, showing an error message on failure."""
    try:
        student.remove_grade_by_value(grade)
        print(f"Grade {grade} removed.")
    except ValueError as error:
        print(f"Error: {error}")


def remove_by_index_safely(student, index):
    """Remove a grade by index, showing an error message on failure."""
    try:
        student.remove_grade_by_index(index)
        print(f"Grade at index {index} removed.")
    except IndexError as error:
        print(f"Error: {error}")


def main():
    """Run a demonstration of the grade management system."""
    print("--- Invalid students ---")
    create_student("", "Ana")
    create_student("S002", None)

    print("\n--- Valid student ---")
    student = create_student("S001", "Luis Luna")
    if student is None:
        return

    for grade in (95.0, 88.5, 100, 92.0):
        add_grade_safely(student, grade)

    print("\n--- Invalid grades ---")
    add_grade_safely(student, "Ninety")
    add_grade_safely(student, 150)
    add_grade_safely(student, -5)

    print("\n--- Removing grades ---")
    remove_by_value_safely(student, 88.5)
    remove_by_value_safely(student, 50.0)
    remove_by_index_safely(student, 1)
    remove_by_index_safely(student, 9)

    print()
    print(student.generate_report())


if __name__ == "__main__":
    main()
