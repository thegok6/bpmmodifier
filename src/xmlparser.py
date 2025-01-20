import xml.etree.ElementTree as ET
from graphviz import Digraph

xml_file = 'xml/Diagram.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

# Namespace in the XML file
namespace = {'ns': 'http://www.wfmc.org/2009/XPDL2.2'}

# Create a Graphviz Digraph object
dot = Digraph(format='png')
dot.attr(rankdir='LR')  # Set the graph direction to Left-to-Right

# Parse Activities and Add Nodes
activities = {}
for activity in root.findall(".//ns:Activity", namespace):
    activity_id = activity.attrib.get("Id")
    activity_name = activity.attrib.get("Name", "Unnamed Activity")
    activities[activity_id] = activity_name
    dot.node(activity_id, activity_name)

# Parse Associations and Add Edges
for association in root.findall(".//ns:Association", namespace):
    source = association.attrib.get("Source")
    target = association.attrib.get("Target")
    if source in activities and target in activities:
        dot.edge(source, target)

# Save and render the diagram
output_file = 'xmlflow'
dot.render(output_file)
print(f"Workflow diagram saved as {output_file}.png")