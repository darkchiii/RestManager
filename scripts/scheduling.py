#
from ortools.sat.python import cp_model
from datetime import datetime

class Employees:
    def __init__(self, name, preferred_shifts, availability, shift_requests, max_working_hours):
        self.name = name
        self.preferred_shifts = preferred_shifts
        self.availability = availability
        self.shift_requests = shift_requests
        self.max_working_hours = max_working_hours
        self.max_working_days = self.max_working_hours//8

employees = [
    Employees(
        "Ola",
        [0, 1], # 0 - morning shift, 1 - afternoon shift
        {
            0: [0, 1],
            1: [0, 1],
            2: [0, 1],
            3: [0, 1],
            4: [0],
            5: [0],
            6: [0, 1]
        },
        [],
        40
    ),
    Employees(
        "Marek",
        [0, 1],
        {
            0: [0, 1],
            1: [0],
            2: [0],
            3: [0],
            4: [],
            5: [0, 1],
            6: [],
        },
        [],
        30
    ),
    Employees(
        "Kasia",
        [1],
        {
            0: [1],
            1: [],
            2: [0, 1],
            3: [1],
            4: [],
            5: [0, 1],
            6: [0, 1],
        },
        [],
        20
    ),
    Employees(
        "Jan",
        [1],
        {
            0: [],
            1: [1],
            2: [1],
            3: [1],
            4: [1],
            5: [1],
            6: []
        },
        [],
        16
    ),
    Employees(
        "Zosia",
        [1],
        {
            0: [],
            1: [],
            2: [1],
            3: [1],
            4: [1],
            5: [],
            6: [],
        },
        [],
        16
    ),
    Employees(
        "Grzegorz",
        [0, 1],
        {
            0: [0, 1],
            1: [0, 1],
            2: [0, 1],
            3: [0, 1],
            4: [0],
            5: [0],
            6: [0, 1]
        },
        [],
        32
    ),
    # Employees(
    #     "Ania",
    #     [0, 1],
    #     {
    #         0: [],
    #         1: [],
    #         2: [0, 1],
    #         3: [0, 1],
    #         4: [0, 1],
    #         5: [0, 1],
    #         6: [0, 1]
    #     },
    #     [],
    #     40
    # ),
    Employees(
        "Krzysiek",
        [0, 1],
        {
            0: [0, 1],
            1: [0, 1],
            2: [0, 1],
            3: [0, 1],
            4: [0],
            5: [0],
            6: [0, 1]
        },
        [],
        32
    ),
]

# employees = [
#     Employees(
#         "Alice",
#         [0, 1],  # Może pracować zarówno na zmianie 0 jak i 1
#         {
#             0: [0, 1],  # Poniedziałek: dostępna na zmianie 0 i 1
#             1: [0],     # Wtorek: dostępna tylko na zmianie 0
#             2: [0, 1],  # Środa: dostępna na zmianie 0 i 1
#             3: [0],     # Czwartek: dostępna tylko na zmianie 0
#             4: [0],     # Piątek: dostępna tylko na zmianie 0
#             5: [0, 1],  # Sobota: dostępna na zmianie 0 i 1
#             6: [0, 1]   # Niedziela: dostępna na zmianie 0 i 1
#         },
#         [],  # Brak zgłoszonych preferencji zmian (shift_requests)
#         32  # Alice może pracować maksymalnie 32 godziny tygodniowo
#     ),
#     Employees(
#         "Bob",
#         [0],  # Preferuje tylko zmianę 0
#         {
#             0: [0],  # Poniedziałek: dostępny tylko na zmianie 0
#             1: [0],  # Wtorek: dostępny tylko na zmianie 0
#             2: [0],  # Środa: dostępny tylko na zmianie 0
#             3: [],    # Czwartek: niedostępny
#             4: [0],   # Piątek: dostępny tylko na zmianie 0
#             5: [],    # Sobota: niedostępny
#             6: []     # Niedziela: niedostępny
#         },
#         [],  # Brak zgłoszonych preferencji zmian
#         24  # Bob może pracować maksymalnie 24 godziny tygodniowo
#     ),
#     Employees(
#         "Charlie",
#         [1],  # Preferuje tylko zmianę 1
#         {
#             0: [],   # Poniedziałek: niedostępny
#             1: [1],  # Wtorek: dostępny tylko na zmianie 1
#             2: [1],  # Środa: dostępny tylko na zmianie 1
#             3: [1],  # Czwartek: dostępny tylko na zmianie 1
#             4: [],   # Piątek: niedostępny
#             5: [1],  # Sobota: dostępny tylko na zmianie 1
#             6: []    # Niedziela: niedostępny
#         },
#         [],  # Brak zgłoszonych preferencji zmian
#         40  # Charlie może pracować maksymalnie 40 godzin tygodniowo
#     ),
#     Employees(
#         "Diana",
#         [0, 1],  # Może pracować na zmianach 0 i 1
#         {
#             0: [0, 1],  # Poniedziałek: dostępna na zmianie 0 i 1
#             1: [0, 1],  # Wtorek: dostępna na zmianie 0 i 1
#             2: [0, 1],  # Środa: dostępna na zmianie 0 i 1
#             3: [0, 1],  # Czwartek: dostępna na zmianie 0 i 1
#             4: [],       # Piątek: niedostępna
#             5: [],       # Sobota: niedostępna
#             6: [0, 1]    # Niedziela: dostępna na zmianie 0 i 1
#         },
#         [],  # Brak zgłoszonych preferencji zmian
#         40  # Diana może pracować maksymalnie 40 godzin tygodniowo
#     ),
#     Employees(
#         "Eve",
#         [0],  # Preferuje tylko zmianę 0
#         {
#             0: [0],  # Poniedziałek: dostępna tylko na zmianie 0
#             1: [],    # Wtorek: niedostępna
#             2: [0],   # Środa: dostępna tylko na zmianie 0
#             3: [],    # Czwartek: niedostępna
#             4: [0],   # Piątek: dostępna tylko na zmianie 0
#             5: [0],   # Sobota: dostępna tylko na zmianie 0
#             6: []     # Niedziela: niedostępna
#         },
#         [],  # Brak zgłoszonych preferencji zmian
#         32  # Eve może pracować maksymalnie 32 godziny tygodniowo
#     ),
#     Employees(
#         "Frank",
#         [1],  # Preferuje tylko zmianę 1
#         {
#             0: [],   # Poniedziałek: niedostępny
#             1: [1],  # Wtorek: dostępny tylko na zmianie 1
#             2: [1],  # Środa: dostępny tylko na zmianie 1
#             3: [],   # Czwartek: niedostępny
#             4: [1],  # Piątek: dostępny tylko na zmianie 1
#             5: [1],  # Sobota: dostępny tylko na zmianie 1
#             6: []    # Niedziela: niedostępny
#         },
#         [],  # Brak zgłoszonych preferencji zmian
#         24  # Frank może pracować maksymalnie 40 godzin tygodniowo
#     ),
# ]


shifts_type = [0, 1]
num_employees = len(employees)
all_employees = range(num_employees)
all_shifts = range(2)
all_days = range(7)
shifts_per_day = 1
weekly_cover_demands = [
(1, 2),
(2, 2),
(1, 2),
(2, 2),
(2, 2),
(2, 2),
(2, 1),
]

# Solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

def demand_for_employees():
    start_m_shift = '07:00:00'
    end_m_shift = '15:00:00'
    start_a_shift = '14:30:00'
    end_a_shift = '21:00:00'
    FMT = '%H:%M:%S'
    morning_shift_duration = (datetime.strptime(end_m_shift, FMT) - datetime.strptime(start_m_shift, FMT)).total_seconds()/3600
    afternoon_shift_duration = (datetime.strptime(end_a_shift, FMT) - datetime.strptime(start_a_shift, FMT)).total_seconds()/3600
    working_hours = 0
    employees_available_hours = 0

    for e in employees:
        employees_available_hours += e.max_working_hours

    for j in range(len(weekly_cover_demands)):
        for i in range(len(shifts_type)):
            if i == 0:
                working_hours += weekly_cover_demands[j][i]*morning_shift_duration
            if i == 1:
                working_hours += weekly_cover_demands[j][i]*afternoon_shift_duration

    print(f"Working hours after considering shift cover demands: {working_hours}")
    print(f"Employees available hours: {employees_available_hours}")

def max_consecutive_days_allowed(MDaysPerWeek):
    if MDaysPerWeek == 5:
        return 3
    elif MDaysPerWeek == 4:
        return 3
    elif MDaysPerWeek == 3:
        return 2
    elif MDaysPerWeek == 2:
        return 2
    elif MDaysPerWeek == 1:
        return 1
    else:
        return 0

class MultipleSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, shifts, employees, all_days,
                 all_shifts, solution_limit=3):
        super().__init__()
        self.shifts = shifts
        self.employees = employees
        self.all_days = all_days
        self.all_shifts = all_shifts
        self.solution_count = 0
        self.solution_limit = solution_limit

    def on_solution_callback(self):
        self.solution_count += 1
        print(f"\n Rozwiązanie {self.solution_count}")

        for d in self.all_days:
            print(f"Dzień {d+1}")
            for e, employee in enumerate(self.employees):
                for s in self.all_shifts:
                    if self.Value(self.shifts[(e, d, s)]) == 1:
                        print(f" {employee.name} pracuje na zmianie {s}")

        if self.solution_count >= self.solution_limit:
            print(f"Solution limit reached.")
            self.StopSearch()

def new_schedule():
    print(demand_for_employees())

# Creating empty matrix for employees work schedule
    print("Creating 'shifts' variables.")
    shifts = {}

    for e in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts[(e,d,s)] = model.NewBoolVar(f"shift_e{e}_d{d}_s{s}")

# Each employee works at most one shift per day
    print("Adding one shift per day rule...")
    for e in all_employees:
        for d in all_days:
            # print(f"Employee {e}, Day {d}: ", [shifts[(e, d, s)] for s in all_shifts])
            model.AddAtMostOne([shifts[(e, d, s)] for s in all_shifts])
    print("Added.")

# Enforcing num of employees per shift according to cover demands
    print("Adding cover demand rule...")
    for d, demands in enumerate(weekly_cover_demands):
        for s, required_workers in enumerate(demands):
            model.Add(sum(shifts[(e, d, s)] for e in all_employees) == required_workers)
    print("Added.")

# Ensuring employees work only when they are available
    print("Adding works only when available rule...")
    for e, employee in enumerate(employees):
        print(f"{employee.name} availability: {employee.availability}")
        for d in all_days:
            # shifts_available = employee.availability.get(d, [])
            for s in all_shifts:
                if s not in employee.availability.get(d, []):
                    print(f"Checking: {employee.name}, day {d}, shift {s} - Allowed shifts: {employee.availability.get(d, [])}")
                    model.Add(shifts[(e, d, s)] == 0)
                    print(f"Restriction added, {employee.name} cant work on day {d}, shift {s}")
        # print(f"After restriction: Employee {employee.name}, Day {d}, Shift {s} - Shift value: {solver.Value(shifts[(e, d, s)])}")
        # model.Add(shifts[(0, 4, 1)] == 1)  # np. zmiana 1 w dzień 4, na którą Ola nie może pracować
        print("Added.")

#Maximizing declared working hours
    print("Adding and maximizing declared working hours per week...")
    total_worked_hours = {}
    # for e, employee in enumerate(employees):
        # total_worked_hours[e] = model.NewIntVar(0, employee.max_working_hours, f"worked_hours_{employees[e].name}")

    for e, employee in enumerate(employees):
        shift_durations = {
            0: 480,
            1: 390
        }
        worked_hours_expr = sum(
        shifts[(e, d, s)] * (shift_durations[s]//60) for d in all_days for s in all_shifts
        )

        worked_hours = model.NewIntVar(0, employee.max_working_hours, f"worked_hours_in_hours_{employees[e].name}")
        model.Add(worked_hours == worked_hours_expr)
        total_worked_hours[e] = worked_hours

    model.Maximize(sum(total_worked_hours[e] for e in range(len(employees))))
    print("Added.")

#TO DO: Testing
# Ensuring balance in consecutive working days
    print("Adding consecutive working days restrictions...")
    for e, employee in enumerate(employees):

        max_days_per_week = employee.max_working_days
        max_consecutive_days = max_consecutive_days_allowed(max_days_per_week)

        works = [model.NewBoolVar(f"works_{e}_{d}") for d in all_days]

        for d in range(len(all_days)-max_consecutive_days):
            model.Add(sum(works[d:d+max_consecutive_days]) <= max_consecutive_days)
    print("Added.")

# Ensuring employees work max 5 days in a week
    print("Adding max 5 working days in a week rule...")
    for e, employee in enumerate(employees):
        maxDaysPerWeek = 5
        worked_days = []

        for d in all_days:
            worked_today = model.NewBoolVar(f"worked_e{e}_d{d}")
            model.Add(worked_today == sum(shifts[(e, d, s)] for s in all_shifts))
            worked_days.append(worked_today)

        model.Add(sum(worked_days) <= maxDaysPerWeek)
    print("Added..")


# Maximize shift assignments consistent with preferences
# TO DO: change preference score
    print("Adding maximize shift assignments consistent with preferences...")
    preference_score = model.NewIntVar(0, 35, "preference_score")
    preferred_assignments = []

    for e, employee in enumerate(employees):
        for d in all_days:
            for s in all_shifts:
                if s in employee.preferred_shifts:
                    preferred_assignments.append(shifts[e, d, s])

    model.Add(preference_score == sum(preferred_assignments))
    model.Maximize(preference_score)
    print("Added.")

    #For testing purpose
    # return shifts

    solution_printer = MultipleSolutionPrinter(shifts, employees, all_days, all_shifts, solution_limit=5)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for e in all_employees:
            print(f"Total worked hours for employee {employees[e].name}: {solver.Value(total_worked_hours[e])}")
    else:
        print("No solution found.")

    if solution_printer.solution_count == 0:
        print("Nie znaleziono żadnych rozwiązań.")
    else:
        print(f"Znaleziono {solution_printer.solution_count} rozwiązanie/rozwiązań.")


if __name__ == "__main__":
    new_schedule()
