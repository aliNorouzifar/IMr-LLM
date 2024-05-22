
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import time
import pm4py
from pm4py.objects.log import obj as log_instance
from local_pm4py import discovery
from local_pm4py.declare.discovery import discover_declare
from local_pm4py.functions import parse_rules


support = 0.2
ratio = 0
logP = xes_importer.apply(r"C:\Users\kourani\PycharmProjects\IMr-LLM\files\01_running-example.xes")

activities = list(pm4py.get_event_attribute_values(logP, attribute="concept:name").keys())
print(activities)

logM = log_instance.EventLog()
logM.append(log_instance.Trace())

# conf = 1
# print(f'conf: {conf}')
# rules = discover_declare(logP, min_support_ratio=1 - conf, min_confidence_ratio=conf,allowed_templates=allowed_templates)
# for r in allowed_templates:
#     if r not in rules.keys():
#         rules[r] = []


rules_file = r"C:\Users\kourani\PycharmProjects\IMr-LLM\files\rules.txt"
rules = parse_rules.parse_constraints(rules_file, activities)


start = time.time()
net, initial_marking, final_marking = discovery.apply_bi(logP,logM, sup=support, ratio=ratio, size_par=len(logP)/max(1,len(logM)),rules = rules)
end = time.time()

print("run time:")
print(end-start)

parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT:"png"}
gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
pn_visualizer.view(gviz)

# file_name = "petri_r"+str(ratio)+"_s"+str(support)
# pm4py.write_pnml(net, initial_marking, final_marking, file_name)


