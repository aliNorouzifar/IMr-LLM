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


def parse_constraints(file_path, log_activities):
    constraints_dict = {v[0]: [] for v in constraint_key_dict.values()}

    with open(file_path, 'r') as file:
        lines = file.readlines()

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
