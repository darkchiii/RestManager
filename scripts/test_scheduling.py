from scheduling import solver, model, weekly_cover_demands, all_days, all_shifts, all_employees, new_schedule
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



if __name__ == "__main__":
    test_cover_demand_rule()
    test_one_shift_per_day_rule()