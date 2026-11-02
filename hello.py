class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_avg_grade(self):
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.get_avg_grade():.1f}"

    def __lt__(self, other):
        return self.get_avg_grade() < other.get_avg_grade()

    def __gt__(self, other):
        return self.get_avg_grade() > other.get_avg_grade()

    def __eq__(self, other):
        return self.get_avg_grade() == other.get_avg_grade()

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка'
        if course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_avg_hw(self):
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        courses_in_progress_str = ", ".join(self.courses_in_progress)
        finished_courses_str = ", ".join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self.get_avg_hw():.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress_str}\n"
                f"Завершенные курсы: {finished_courses_str}")

    def __lt__(self, other):
        return self.get_avg_hw() < other.get_avg_hw()

    def __gt__(self, other):
        return self.get_avg_hw() > other.get_avg_hw()

    def __eq__(self, other):
        return self.get_avg_hw() == other.get_avg_hw()

def get_students_avg_hw(students_list, course_name):
    total_grades = []
    for student in students_list:
        if course_name in student.grades:
            total_grades.extend(student.grades[course_name])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)

def get_lecturers_avg_lecture(lecturers_list, course_name):
    total_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            total_grades.extend(lecturer.grades[course_name])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)

if __name__ == '__main__':
    lecturer_1 = Lecturer('Иван', 'Иванов')
    lecturer_2 = Lecturer('Мария', 'Сидорова')
    reviewer_1 = Reviewer('Пётр', 'Петров')
    reviewer_2 = Reviewer('Анна', 'Смирнова')
    student_1 = Student('Ольга', 'Алёхина', 'Ж')
    student_2 = Student('Дмитрий', 'Козлов', 'М')

    lecturer_1.courses_attached += ['Python', 'Java']
    lecturer_2.courses_attached += ['Python', 'C++']
    reviewer_1.courses_attached += ['Python', 'Java']
    reviewer_2.courses_attached += ['Python', 'C++']
    student_1.courses_in_progress += ['Python', 'Java']
    student_2.courses_in_progress += ['Python', 'C++']

    reviewer_1.rate_hw(student_1, 'Python', 9)
    reviewer_1.rate_hw(student_1, 'Python', 10)
    reviewer_1.rate_hw(student_1, 'Java', 8)
    reviewer_2.rate_hw(student_2, 'Python', 7)
    reviewer_2.rate_hw(student_2, 'C++', 9)

    student_1.rate_lecture(lecturer_1, 'Python', 10)
    student_1.rate_lecture(lecturer_1, 'Java', 9)
    student_2.rate_lecture(lecturer_2, 'Python', 8)
    student_2.rate_lecture(lecturer_2, 'C++', 9)

    print("--- Студент ---")
    print(student_1)
    print("\n--- Лектор ---")
    print(lecturer_1)
    print("\n--- Ревьюер ---")
    print(reviewer_1)

    print("\nЛектор 1 лучше Лектора 2?", lecturer_1 > lecturer_2)

    print("\nСредняя оценка студентов по Python:", get_students_avg_hw([student_1, student_2], 'Python'))
    print("Средняя оценка лекторов по Python:", get_lecturers_avg_lecture([lecturer_1, lecturer_2], 'Python'))