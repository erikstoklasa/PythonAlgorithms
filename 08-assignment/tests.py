import paths
import os

files = os.listdir("./hw08examples")
filtered_files = list()
test_list = list()

for f in files:
    if f.startswith("case") and f.endswith(".txt"):
        filtered_files.append(f)

for f in filtered_files:
    fn_list = f[:-4].split("-")
    if len(fn_list) > 2 and fn_list[2] == "solution":
        test_list.append((f"case-{fn_list[1]}.txt", f))

tests_failed = False
failed = list()
passed = list()
print(f"Starting {len(test_list)} tests...")
for i in range(len(test_list)):
    test_case, test_solution = test_list[i]
    computed_solution = paths.computePaths("./hw08examples/" + test_case)
    solution_file = open("./hw08examples/" + test_solution, "r")
    solutions_list = tuple(map(int, solution_file.readline().split()))
    current_failed = False
    for y in range(len(solutions_list)):
        if computed_solution[y] != solutions_list[y]:
            current_failed = True
    if current_failed:
        failed.append((test_case, solutions_list, computed_solution, False))
    else:
        passed.append((test_case, solutions_list, computed_solution, True))
    solution_file.close()

if len(passed) == len(test_list):
    print("Passed all tests")
else:
    for (test_case, solutions_list, computed_solution, passed_test) in failed:
        print(f"{'Error in file:':<20}{test_case}")
        print(f"{'Should return:':<20}{solutions_list}")
        print(f"{'Returned:':<20}{computed_solution}")
        print()
    print(f"PASSED {len(passed)}/{len(test_list)}")
