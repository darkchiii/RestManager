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
        [0], # 0 - morning shift, 1 - afternoon shift
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
    # Employees(
    #     "Marek",
    #     [0],
    #     {
    #         0: [0],
    #         1: [0],
    #         2: [0],
    #         3: [0],
    #         4: [],
    #         5: [0],
    #         6: [],
    #     },
    #     [],
    #     32
    # ),
    Employees(
        "Kasia",
        [1],
        {
            0: [0, 1],
            1: [],
            2: [],
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
        24
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
    Employees(
        "Ania",
        [0, 1],
        {
            0: [],
            1: [],
            2: [0, 1],
            3: [0, 1],
            4: [0, 1],
            5: [0, 1],
            6: [0, 1]
        },
        [],
        40
    ),
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

def DemandForEmployees():
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

class MultipleSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, shifts, employees, all_days,
                 all_shifts, max_solutions=3):
        super().__init__()
        self.shifts = shifts
        self.employees = employees
        self.all_days = all_days
        self.all_shifts = all_shifts
        self.solution_count = 0
        self.max_solutions = max_solutions

    def on_solution_callback(self):
        print(f"\n Rozwiązanie {self.solution_count+1}")
        for d in self.all_days:
            print(f"Dzień {d+1}")
            for e, employee in enumerate(self.employees):
                for s in self.all_shifts:
                    if self.Value(self.shifts[(e, d, s)]) == 1:
                        print(f" {employee.name} pracuje na zmianie {s}")
        self.solution_count += 1

        if self.solution_count >= self.max_solutions:
            print(f"Ilość rozwiązań {self.solution_count}")
            self.StopSearch()
            print(f"Ilość rozwiązań {self.solution_count}")
            return

def new_schedule():
    model = cp_model.CpModel()

    print(DemandForEmployees())

    # Creating empty matrix for employees work schedule
    print("Creating 'shifts' variables.")
    shifts = {}
    for e in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts[(e,d,s)] = model.NewBoolVar(f"shift_e{e}_d{d}_s{s}")
    # print("Shifts created : ", shifts)

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

    # Ensuring balance in consecutive working days
    print("Adding consecutive working days restrictions...")
    for e, employee in enumerate(employees):
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

# Ensuring employees work only when they are available
    print("Adding works only when available rule...")
    for e, employee in enumerate(employees):
        max_days = employee.max_working_days
        worked_days = []

        for d in all_days:
            shifts_available = employee.availability.get(d, [])
            for s in all_shifts:
                if s not in shifts_available:
                    model.Add(shifts[(e, d, s)] == 0)
        print("Added.")

# Ensuring employee don't exceed their declared max working hours per week
        print("Adding max working hours per week rule...")
        for d in all_days:
            worked_today = model.NewBoolVar(f"worked_{e}_{d}")
            model.AddMaxEquality(worked_today, [shifts[(e, d, s)] for s in all_shifts])
            worked_days.append(worked_today)
        model.Add(sum(worked_days) <= max_days)
    print("Added..")

# Maximize shift assignments consistent with preferences
    #TO DO: change preference score
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

    # Randomly changing prorities - to delete, don't consider restrictions
    # model.Maximize(sum(shifts[(e, d, s)] * (e + d + s) for e in all_employees for d in all_days for s in all_shifts))

#TO DO: Balance weekend shifts
#TO DO: Minimal rest time between shifts
#TO DO: Considering employees required shifts

# Create and run solver
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solution_printer = MultipleSolutionPrinter(shifts, employees, all_days, all_shifts, max_solutions=10)
    status = solver.SolveWithSolutionCallback(model, solution_printer)
    # print(f"enumerate_all_solutions: {solver.parameters.enumerate_all_solutions}")
    # print(f"Maksymalna liczba rozwiązań: {solution_printer.max_solutions}")

    # print("\nDebugging: Wartości zmiennych przed rozwiązaniem")
    # for d in all_days:
    #     for e, employee in enumerate(employees):
    #         for s in all_shifts:
    #             val = solver.Value(shifts[(e, d, s)])
    #             print(f"shift_e{e}_d{d}_s{s} = {val}")

    if solution_printer.solution_count == 0:
        print("Nie znaleziono rozwiązania.")

if __name__ == "__main__":
    new_schedule()

