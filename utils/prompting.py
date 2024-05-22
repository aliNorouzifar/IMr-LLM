def create_inital_prompt(log_activities, description):
    prompt = ''
    prompt += role_prompt() + '\n\n'
    prompt += inject_knowledge() + '\n\n'
    prompt += add_examples() + '\n\n'
    prompt += add_more_info() + '\n\n'
    prompt += add_activities(log_activities) + '\n\n'
    prompt += add_description(description) + '\n\n'
    prompt += final_instructs()

    return prompt


def role_prompt():
    return "- Process discovery is a type of process mining aiming to represent the process model explaining how the " \
           "process is executed. Our focus is on the discovery of an imperative process model. Recently, we developed " \
           "a framework that allows for some declarative constraints as input to discover better imperative models. " \
           "Declarative models are close to the natural language, however for a domain expert, they might not be " \
           "familiar. Therefore, we need your help to translate the process description given as a text to the " \
           "declarative constraints we need for the discovery of imperative process models. "


def inject_knowledge():
    return """Consider only the following declarative constraint definitions:
"
* at-most(a): a occurs at most once. These sequence of activities satisfy this constraint: <b,c,c>, <b,c,a,c>,<b,a>,<b,b,c,c,d,a>. These sequence of activities this constraint: <b,c,a,a,c>, <b,c,a,c,a,a>,<a,a>,<b,c,d,a,a,a>.

* existence(a): a occurs at least once. These sequence of activities satisfy this constraint: <b,c,a>, <b,a,c,a>,<b,a,a>,<b,b,c,c,d,a>. These sequence of activities violate this constraint: <b,c>, <b,a,c>,<b,c,c>,<b,c,d>,<e,d,b,c>.

* response(a,b): If a occurs, then b occurs after a. These sequence of activities satisfy this constraint: <c,a,a,c,b>, <b,c,c>,<a,b,c,d>,<a,a,a,b>,<b,c,c,d>. These examples violate this constraint: <c,a,a,c>, <b,a,c,c>,<c,c,a>,<a,a,c,d>,<e,d,a,a,a,c>.

* precedence(a,b): b occurs only if preceded by a. These sequence of activities satisfy this constraint: <c,a,c,b,b>, <a,c,c>,<b,a,c,d>,<b,b,b,b,a>,<b,b,c,c,d>. These examples sequence of activities this constraint: <c,c,b,b>, <b,a,c,c>,<c,c,a,b>,<a,a,c,d>,<e,d,a,b,c>.

* co-existence(a,b): a and b occur together. These sequence of activities satisfy this constraint: <c,a,c,b,b>, <b,c,c,a>,<a,b>,<a,b,c,c,d,b,b,b>,<c,d,e>. These sequence of activities violate this constraint: <c,a,c>, <b,c,c>,<b,b,c,d>,<c,c,a>,<e,d,a,a,a,c>.

* not-co-existence(a,b): a and b never occur together. These sequence of activities satisfy this constraint: <c,c,c,b,b,b>, <c,c,a,c>,<a,a,c,c>,<b,b,c,c,b,d>,<c,d,e>. These sequence of activities violate this constraint: <a,c,c,b,b>, <b,c,a,c>,<a,a,b,c,c>,<a,b,b,b,c,d>.

* not-succession(a,b): b cannot occur after a. These sequence of activities satisfy this constraint: <b,b,c,a,a>, <c,b,b,c,a>,<b,b,a,a,c,c>,<b,b,c,c,b,a,d>. These sequence of activities violate this constraint: <a,a,c,b,b>, <a,b,b>,<a,a,b,b,c,c>,<a,b,b,c,d>.

* responded-existence(a,b): If a occurs in the trace, then b occurs as well. These sequence of activities satisfy this constraint: <b,c,a,a,c>, <b,c,c>,<a,b>,<a,b,c,c,d,a,a,a>. These sequence of activities violate this constraint: <c,a,a,c>, <a,c,c>,<c,c,a>,<a,a,c,d>,<e,d,a,a,a,c>.
    """


def add_examples():
    return """Some examples of mapping between natural language and declarative constraints:
*example 1: “in our process activities a and b cannot occur together”, constraint not-co-existence(a,b) corresponds to this statement.
* example 2: “each client in this process has the outcome a or b as the final decision” ”, constraint not-co-existence(a,b) corresponds to this statement.
*example 3: “all the costumers start the process with activity a”, constraint existence(a) corresponds to this statement.
*example 4: “after execution of activity a, some cases will continue with activity b and some cases will continue with activity c”, constraints precedence (a,b), precedence(a,c), not-succession(b,a), not-succession(c,a)  correspond to this statement.
*example 5: all the occurrences of activity a should be followed by activity b, constraint response(a,b) corresponds to this statement.
    """


def add_more_info():
    return """Some more instructions:
* It is not possible to generate constraints like response(a, (b or c)). The first and second elements must be a single activity


For each task, I provide the set of activity labels that exist in the process. Then, I present a text written by a process expert and want you to translate it to declarative constraints and write it in a plaintext block."""


def add_activities(activities):
    return "This is the set of activities: {" + ", ".join(activities) + "}."


def add_description(description):
    return f"This is the process description: {description}"


def final_instructs():
    return """Now extract declarative rules and write them in formal language in a text block starting with the tag START``` and ending with the tag ```END (I need to extract them using the pattern pattern r"START```(.*?)```END"). Please put each rule in a seperate line and don't add any descriptions or any additional information."""
