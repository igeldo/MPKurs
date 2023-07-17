class BachelorStudent:
    def __init__(self, first_name, last_name, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self._birthday = birthday
        self.__start_date = 20201001
        self.student_id = self._compute_student_id()

    def _compute_student_id(self):
        return self.__start_date - self._birthday

    def display_info(self):
        print("Student Information:")
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Degree: {self.__class__.__name__}")
        print(f"Start date: {self.__start_date}")
        print(f"Student ID: {self.student_id}\n")

class MasterStudent(BachelorStudent):
    def __init__(self, first_name, last_name, birthday):
        super().__init__(first_name, last_name, birthday)
        self.__start_date = 20231001

juroe = BachelorStudent(first_name='Julian', last_name='Roemer', birthday=19890927)
juroeM = MasterStudent(first_name='Julian', last_name='Roemer', birthday=19890927)

juroe.display_info()
juroeM.display_info()

print(juroe._BachelorStudent__start_date)
print(juroe.student_id)

print(juroeM._BachelorStudent__start_date)

print(juroeM._MasterStudent__start_date)
print(juroeM.student_id)
