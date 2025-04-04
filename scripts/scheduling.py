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
(1, 2),
(2, 2),
(2, 2),
(2, 2),
(2, 1),
]

# Solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

def schedule_diagnosis():
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

    for d, (morning_demand, afternoon_demand) in enumerate(weekly_cover_demands):
        print(f"\nDzień {d+1}")

        morning_availability = [emp.name for emp in employees if 0 in emp.availability.get(d, [])]
        afternoon_availability = [emp.name for emp in employees if 1 in emp.availability.get(d, [])]

        if len(morning_availability) < morning_demand:
            print(f"\n ! Dzień {d+1} rano: dostępni: {len(morning_availability)}, {morning_availability}, zapotrzebowanie: {morning_demand}.")
        elif len(afternoon_availability) < afternoon_demand:
            print(f"\n ! Dzień {d+1} południe: dostępni: {len(afternoon_availability)}, {afternoon_availability}, zapotrzebowanie: {afternoon_demand}.")
        else:
            print("Dyspozycja pokrywa zapotrzebowanie.")

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
    schedule_diagnosis()

# Creating empty matrix for employees work schedule
    shifts = {}

    for e in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts[(e,d,s)] = model.NewBoolVar(f"shift_e{e}_d{d}_s{s}")

# Basic constraints
    print("Adding one shift per day rule...")
    for e in all_employees:
        for d in all_days:
            model.AddAtMostOne([shifts[(e, d, s)] for s in all_shifts])
    print("Added.")

# Availability constraints
    print("Adding works only when available rule...")
    for e, employee in enumerate(employees):
        print(f"{employee.name} availability: {employee.availability}")
        for d in all_days:
            shifts_available = employee.availability.get(d, [])
            for s in all_shifts:
                if s not in shifts_available:
                    print(f"Checking: {employee.name}, day {d}, shift {s} - Allowed shifts: {employee.availability.get(d, [])}")
                    model.Add(shifts[(e, d, s)] == 0)
                    print(f"Restriction added, {employee.name} cant work on day {d}, shift {s}")
        print("Added.")

# Coverage of demands
    print("Adding cover demand rule...")
    for d, demands in enumerate(weekly_cover_demands):
        for s, required_workers in enumerate(demands):
            model.Add(sum(shifts[(e, d, s)] for e in all_employees) == required_workers)
    print("Added.")

# Working hours constraints
    print("Adding and maximizing declared working hours per week...")
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
    print("Added.")

#TO DO: Testing
# Consecutive working days constraints
    print("Adding consecutive working days restrictions...")
    for e, employee in enumerate(employees):

        max_days_per_week = employee.max_working_days
        max_consecutive_days = max_consecutive_days_allowed(max_days_per_week)

        works = [model.NewBoolVar(f"works_{e}_{d}") for d in all_days]

        for d in range(len(all_days)-max_consecutive_days):
            model.Add(sum(works[d:d+max_consecutive_days]) <= max_consecutive_days)
    print("Added.")

# Max working days in a week constraints
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

    #For testing purpose
    # return shifts
    print("Liczba ograniczeń:", len(model.Proto().constraints))

    solver.parameters.max_time_in_seconds = 30.0
    solution_printer = MultipleSolutionPrinter(shifts, employees, all_days, all_shifts, 5)
    status = solver.Solve(model, solution_printer)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("\nPodsumowanie godzin:")
        for e in all_employees:
            minutes = solver.Value(total_worked_minutes[e])
            hours = minutes/60
            print(f"Total worked hours for employee {employees[e].name}: {hours}")
            # print(f"{employees[e].name}: {hours}h/{employees[e].max_working_hours}h")
    else:
        print("Nie znaleziono rozwiązania.")
        print("Przyczyny mogą obejmować:")
        print("- Niewystarczająca liczba pracowników")
        print("- Zbyt restrykcyjne ograniczenia dostępności")
        print("- Sprzeczne wymagania")

if __name__ == "__main__":
    new_schedule()
