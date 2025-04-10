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
            0: [0,1],
            # 0: [0, 1],
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
        "Kasia 2",
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
        16
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
(2, 2),
(2, 2),
(1, 2),
(2, 2),
(2, 3),
]

def basic_diagnosis():
# Wyliczanie dostępnych godzin pracowników i zapotrzebowania
    start_m_shift = '07:00:00'
    end_m_shift = '15:00:00'
    start_a_shift = '14:30:00'
    end_a_shift = '21:00:00'
    FMT = '%H:%M:%S'
    morning_shift_duration = (datetime.strptime(end_m_shift, FMT) - datetime.strptime(start_m_shift, FMT)).total_seconds()/3600
    afternoon_shift_duration = (datetime.strptime(end_a_shift, FMT) - datetime.strptime(start_a_shift, FMT)).total_seconds()/3600

    total_hours_needed = sum(morning_shift_duration * morning + afternoon_shift_duration * afternoon for morning, afternoon in weekly_cover_demands)
    total_hours_available = sum(emp.max_working_hours for emp in employees)
    deficit = total_hours_needed - total_hours_available

    if total_hours_available < total_hours_needed:
        print(f"\n ! Brak godzin: potrzebne {total_hours_needed}, dostępne {total_hours_available}, brakuje: {deficit}")
    else:
        print(f"\nWorking hours after considering shift cover demands: {total_hours_needed}")
        print(f"Employees available hours: {total_hours_available}")

# Wyliczanie limitów pracowników
    print("\nLimity pracowników")
    for emp in employees:
        available_days= sum(1 for d in all_days if any(s in emp.availability.get(d, []) for s in all_shifts))
        print(f"{emp.name}: max hours - {emp.max_working_hours}, available days - {available_days}")

def max_consecutive_days_allowed(MDaysPerWeek):
    if MDaysPerWeek == 5:
        return 4
    elif MDaysPerWeek == 4:
        return 3
    elif MDaysPerWeek == 3:
        return 2
    else:
        return MDaysPerWeek

class OptimalSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, shifts, employees, all_days,
                 all_shifts, violations, total_worked_minutes, solution_limit=5):
        super().__init__()
        self.shifts = shifts
        self.employees = employees
        self.all_days = all_days
        self.all_shifts = all_shifts
        self.violations = violations
        self.total_worked_minutes = total_worked_minutes
        self.solution_count = 0
        self.solutions = []
        self.solution_limit = solution_limit

    def on_solution_callback(self):
        self.solution_count += 1

        shortage_score = sum(self.Value(self.violations[f"coverage_d{d}_s{s}"]) for d in self.all_days for s in self.all_shifts)

        total_score = (
            shortage_score * 1000
        )
        total_work = {}
        for e, emp in enumerate(self.employees):
            # print(f"Total worked for {emp.name}: {self.total_worked_minutes[e]}")
            minutes = self.Value(total_worked_minutes[e])
            hours = minutes/60
            total_work[e] = hours
            # print(f"Total worked for {emp.name}: {total_work[e]}")

        # total_worked_hours = self.total_worked_minutes/60

        solution = {
            'shortage': shortage_score,
            'total_worked': total_work,
            'total_score': total_score,
            'solution_id': self.solution_count,
            'values': {(e, d, s): self.Value(self.shifts[(e, d, s)])
                       for e in all_employees
                       for d in self.all_days
                       for s in self.all_shifts
                       }
        }

        self.solutions.append(solution)

        if self.solution_count >= self.solution_limit:
            self.StopSearch()

    def print_sorted_solutions(self):
        self.solutions.sort(key=lambda x: x['total_score'])

        for i, sol in enumerate(self.solutions, 1):
            print(f"\nRozwiązanie {i}, total score: {sol['total_score']}")
            self.print_single_solution(sol)

    def print_single_solution(self, solution):
        for d in all_days:
            print(f"Dzień {d+1}")
            for e, employee in enumerate(employees):
                for s in all_shifts:
                    if solution['values'].get((e, d, s), 0):
                        print(f"{employee.name} pracuje", f"{'na zmianie 0' if s == 0 else 'na zmianie 1'}" )

        print(f"\nGodziny pracy:")
        for e, emp in enumerate(employees):
            print(f"{emp.name} pracuje {solution['total_worked'][e]}h/{emp.max_working_hours}h | {round((solution['total_worked'][e]/emp.max_working_hours) * 100, 2)}% dyspozycji")

    # def get_best_solution(self):
    #     if self.solutions:
    #         return self.solutions[0]
    #     return "Brak najlepszego rozwiązania"

    def solution_count(self):
        return self.solution_count

def build_base_model():
    model = cp_model.CpModel()

    shifts = {}
    for e in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts[(e, d, s)] = model.NewBoolVar(f"shift_e{e}_d{d}_s{s}")
    return model, shifts

def add_hard_constraints(model, shifts):
# One shift per day constraint
    for e in all_employees:
        for d in all_days:
            model.AddAtMostOne([shifts[(e, d, s)] for s in all_shifts])

# Availability constraint
    for e, employee in enumerate(employees):
        # print(f"{employee.name} availability: {employee.availability}")
        for d in all_days:
            shifts_available = employee.availability.get(d, [])
            for s in all_shifts:
                if s not in shifts_available:
                    # print(f"Checking: {employee.name}, day {d}, shift {s} - Allowed shifts: {employee.availability.get(d, [])}")
                    model.Add(shifts[(e, d, s)] == 0)
                    # print(f"Restriction added, {employee.name} cant work on day {d}, shift {s}")

# Max working days in a week constraint
    for e, employee in enumerate(employees):
        maxDaysPerWeek = 5
        worked_days = []

        for d in all_days:
            worked_today = model.NewBoolVar(f"worked_e{e}_d{d}")
            model.Add(worked_today == sum(shifts[(e, d, s)] for s in all_shifts))
            worked_days.append(worked_today)

        model.Add(sum(worked_days) <= maxDaysPerWeek)

# Coverage of demands soft constraint
def add_soft_coverage(model, shifts):
    violations = {}
    for d, (morning_demand, afternoon_demand) in enumerate(weekly_cover_demands):
        for s, demand in enumerate([morning_demand, afternoon_demand]):

            shortage = model.NewIntVar(0, demand, f"shortage_d{d}_s{s}")

            model.Add(sum(shifts[(e,d,s)] for e in all_employees) + shortage == demand)
            violations[f"coverage_d{d}_s{s}"] = shortage
            # model.AddPenalty(shortage, 1000)
    return violations

# Working hours constraint
def add_working_hours_constraint(model, shifts):
    total_worked_minutes = {}
    shift_durations_min = {
        0: 480,  # 8
        1: 390   # 6.5
    }

    for e, employee in enumerate(employees):
        worked_minutes_var = model.NewIntVar(0, employee.max_working_hours * 60, f"worked_minutes_{e}")

        model.Add(
            worked_minutes_var == sum(
                shifts[(e, d, s)] * shift_durations_min[s]
                for d in all_days
                for s in all_shifts
            )
        )
        model.Add(worked_minutes_var <= employee.max_working_hours * 60)
        total_worked_minutes[e] = worked_minutes_var

    model.Maximize(sum(total_worked_minutes[e] for e in range(len(employees))))
    return total_worked_minutes

def add_consecutive_working_days_constraint(model, shifts):
    for e, employee in enumerate(employees):

        max_days_per_week = employee.max_working_days
        max_consecutive_days = max_consecutive_days_allowed(max_days_per_week)

        works = [model.NewBoolVar(f"works_{e}_{d}") for d in all_days]

        for d in range(len(all_days)-max_consecutive_days):
            model.Add(sum(works[d:d+max_consecutive_days]) <= max_consecutive_days)
    # print("Added.")

# Maximize shift assignments consistent with preferences SOFT
def add_shift_preferences(model, shifts):
# TO DO: change preference score
    # print("Adding maximize shift assignments consistent with preferences...")
    # preference_score = model.NewIntVar(0, 35, "preference_score")
    # preferred_assignments = []

    # for e, employee in enumerate(employees):
    #     for d in all_days:
    #         for s in all_shifts:
    #             if s in employee.preferred_shifts:
    #                 preferred_assignments.append(shifts[e, d, s])

    # model.Add(preference_score == sum(preferred_assignments))
    # model.Maximize(preference_score)
    # print("Added.")
    pass

if __name__ == "__main__":
    basic_diagnosis()
    model, shifts = build_base_model()
    add_hard_constraints(model, shifts)
    add_working_hours_constraint(model, shifts)
    total_worked_minutes = add_working_hours_constraint(model, shifts)
    add_consecutive_working_days_constraint(model, shifts)
    violations = add_soft_coverage(model, shifts)
    print("Liczba ograniczeń:", len(model.Proto().constraints))

    solution_printer = OptimalSolutionPrinter(shifts, employees, all_days, all_shifts, violations, total_worked_minutes,  5)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120
    status = solver.Solve(model, solution_printer)
    solution_printer.print_sorted_solutions()

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("\nPodsumowanie naruszeń:")
        any_violations = False
        for d in all_days:
            for s in all_shifts:
                shortage = solver.Value(violations[f"coverage_d{d}_s{s}"])
                print(f"shortage - {shortage}")
                if shortage > 0:
                    any_violations = True
                    print(f"Dzień {d+1}, zmiana {s}: brakuje {shortage} pracowników")

        if not any_violations:
            print("Brak naruszeń, wszystkie zmiany zostały pokryte.")

    else:
        print("Nie znaleziono rozwiązania")
        print(f"- Liczba konfliktów: {solver.num_conflicts}")
        print(f"- Czas: {solver.wall_time}")
        print(f"Znalezine rozwiązania: {solution_printer.solution_count()}")