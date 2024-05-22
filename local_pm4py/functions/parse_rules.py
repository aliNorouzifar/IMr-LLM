import re
import warnings

constraint_key_dict = {
    "at-most": ("atmost1", 1),
    "existence": ("existence", 1),
    "response": ("response", 2),
    "precedence": ("precedence", 2),
    "co-existence": ("coexistence", 2),
    "not-co-existence": ("noncoexistence", 2),
    "not-succession": ("nonsuccession", 2),
    "responded_existence": ("responded_existence", 2),
}


def extract_rules_from_response(response_message):
    pattern = r"START```(.*?)```END"
    match = re.search(pattern, response_message, re.DOTALL)

    if match:
        extracted_text = match.group(1).strip()
        lines = extracted_text.split('\n')
        print("lines: ", lines)
        return lines
    else:
        print(f"Pattern {pattern} not found in th response!")


def parse_constraints_from_file(file_path, log_activities):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        res = parse_constraints(lines)
    return res


def parse_constraints_from_response(response_message, log_activities):
    lines = extract_rules_from_response(response_message)
    return parse_constraints(lines)


def parse_constraints(lines):
    constraints_dict = {v[0]: [] for v in constraint_key_dict.values()}
    line_num = 1
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            warnings.warn("Empty line skipped!")
            continue
        constraint = line.split("(")[0].strip()

        if constraint not in constraint_key_dict.keys():
            raise Exception(f"'{constraint}' in line {line_num} is not a valid constraint key!")

        activities = line[len(f'{constraint}('):-1].split(',')
        activities = tuple(activity.strip() for activity in activities)

        for activity in activities:
            if activity not in log_activities:
                raise Exception(f"Activity '{activity}' used in line {line_num} is not present in the event log!")

        key = constraint_key_dict[constraint][0]
        num_allowed_activities = constraint_key_dict[constraint][1]

        if num_allowed_activities != len(activities):
            raise Exception(f"The constraint '{constraint}' takes {num_allowed_activities} activities,"
                            f" but the number of given activities in line {line_num} is {len(activities)}")

        constraints_dict[key].append(activities)

        line_num = line_num + 1

    return constraints_dict
