from scheduling import solver, model, weekly_cover_demands, all_days, all_shifts, all_employees, employees, new_schedule, max_consecutive_days_allowed
from ortools.sat.python import cp_model
shifts = new_schedule()
if shifts is None:
    raise ValueError("new_schedule returned None.")

def test_one_shift_per_day_rule():
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("test_one_shift_per_day_rule: solved")
        for e in all_employees:
            for d in all_days:
                sum_of_shifts = sum(solver.Value(shifts[(e, d, s)]) for s in all_shifts)
                assert sum_of_shifts <= 1, (
                    f"Test failed for employee {e}, day {d}"
                )
                print(f"Employee {e}, day {d}, sum of shifts {sum_of_shifts}")
        else:
            assert False, "Solver did not find a feasible solution"

def test_cover_demand_rule():
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("test_cover_demand_rule: solved")
        for d, demands in enumerate(weekly_cover_demands):
            for s, required_workers in enumerate(demands):
                assigned_workers = sum(solver.Value(shifts[(e, d, s)]) for e in all_employees)
                assert assigned_workers == required_workers, (
                    f"Test failed for day {d}, shift {s}: required {required_workers}, got {assigned_workers}"
                )
                print(f"Day {d}, Shift {s}: Expected {required_workers}, got {assigned_workers}")
    else:
        assert False, "Solver did not find a feasible solution"

def test_max_working_days_week():
    pass

def test_work_only_when_available():
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("test_work_only_when_available: solved")

    print("Final schedule:")
    for d in all_days:
        print(f"\nDay {d}:")
        for e, employee in enumerate(employees):
            assigned_shifts = []
            for s in all_shifts:
                if (e, d, s) in shifts and solver.Value(shifts[(e, d, s)]) == 1:
                    assigned_shifts.append(s)

            if assigned_shifts:
                print(f"+ {employee.name} → Shifts: {assigned_shifts}")
            else:
                print(f"- {employee.name} is not working.")

        for e, employee in enumerate(employees):
            for d in all_days:
                available_shifts = set(employee.availability.get(d, []))

                for s in all_shifts:
                    if (e, d, s) in shifts:
                        shift_value = solver.Value(shifts[(e, d, s)])
                        if shift_value == 1 and s not in available_shifts:
                        # if s not in employee.availability.get(d, []):
                            print(f"ERROR: {employee.name} is assigned to shift {s} on day {d}, but is not available!")
                            print(f"Available shifts for {employee.name} on day {d}: {available_shifts}")

                            assert False, (f"Test failed: {employee.name} was assigned to shift {s} "
                                       f"on day {d}, but should not be.")
                    else:
                        print(f"WARNING: Missing key ({e}, {d}, {s}) in shifts dictionary.")

        print("Test passed.")

def test_max_working_hours_week():
    pass

# Need to be fixed
def test_consecutive_working_days_limit():
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("test_consecutive_working_days_limit: solved")

        for e, employee in enumerate(employees):
            max_days_per_week = employee.max_working_days
            max_consecutive_days = max_consecutive_days_allowed(max_days_per_week)
            works  = [sum(solver.Value(shifts[(e, d, s)]) for s in all_shifts) > 0 for d in all_days]

            consecutive_days = 0
            max_consecutive_found = 0

            print(f"\n Employee {employee.name} - max {max_consecutive_days} consecutive days allowed")
            print(f"works: {works}")

            for d in all_days:
                if works[d] > 0:
                    consecutive_days += 1
                    max_consecutive_found = max(consecutive_days, max_consecutive_found)
                else:
                    consecutive_days = 0

            assert max_consecutive_found <= max_consecutive_days, (
                f"Test failed, employee {employee.name} got: {max_consecutive_found} consecutive days, max expected days: {max_consecutive_days}"
            )
            print(f"Employee {employee.name} got: {max_consecutive_found} consecutive days, allowed days: {max_consecutive_days}")
    else:
        assert False, "Solver did not find a feasible solution"


if __name__ == "__main__":
    # test_cover_demand_rule()
    # test_one_shift_per_day_rule()
    # test_consecutive_working_days_limit()
    test_work_only_when_available()