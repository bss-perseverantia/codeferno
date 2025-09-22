import os
import random

def is_power_of_two(x):
    return (x & (x - 1)) == 0 and x > 0

def generate_testcase(group_id):
    # Subtask constraints
    if group_id == 0:
        b = random.randint(0, 100)
    elif group_id == 1:
        b = random.randint(0, 10**5)
    elif group_id == 2:
        e = random.randint(0, 30)
        b = 1 << e
    elif group_id == 3:
        b = random.randint(0, 10**9)
    a = random.randint(1, 10**9)
    m = random.randint(1, 10**9)
    return a, b, m

# Ensure directories exist
os.makedirs("../input", exist_ok=True)
os.makedirs("../output", exist_ok=True)

# 4 groups × 10 = 40 testcases
for group in range(4):
    for i in range(10):
        idx = group * 10 + i
        a, b, m = generate_testcase(group)
        
        input_file = f"../input/input{idx}.txt"
        output_file = f"../output/output{idx}.txt"
        
        with open(input_file, "w") as f:
            f.write(f"1\n{a} {b} {m}\n")

        result = pow(a, b, m)
        with open(output_file, "w") as f:
            f.write(f"{result}\n")

print("Generated 40 testcases (input0–input39, output0–output39)")
