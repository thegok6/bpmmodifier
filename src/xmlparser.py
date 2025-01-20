import xml.etree.ElementTree as ET
import dash
from dash import html
import dash_cytoscape as cyto

# Load the XML file
xml_file = '/mnt/data/Diagram.xml'  # Replace with your XML file path
tree = ET.parse(xml_file)
root = tree.getroot()

# Namespace in the XML file
namespace = {'ns': 'http://www.wfmc.org/2009/XPDL2.2'}

# Parse Activities to Create Nodes
nodes = []
for activity in root.findall(".//ns:Activity", namespace):
    activity_id = activity.attrib.get("Id")
    activity_name = activity.attrib.get("Name", "Unnamed Activity")
    nodes.append({"data": {"id": activity_id, "label": activity_name}})

# Parse Associations to Create Edges
edges = []
for association in root.findall(".//ns:Association", namespace):
    source = association.attrib.get("Source")
    target = association.attrib.get("Target")
    if source and target:
        edges.append({"data": {"source": source, "target": target}})

# Combine Nodes and Edges for Cytoscape
elements = nodes + edges

# Create a Dash App
app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'cose'},  # Layout for auto-arrangement
        style={'width': '100%', 'height': '600px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'width': '50px',
                    'height': '50px',
                    'background-color': '#0074D9',
                    'color': '#ffffff',
                    'text-valign': 'center',
                    'text-halign': 'center',
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 2,
                    'line-color': '#7FDBFF',
                    'target-arrow-color': '#7FDBFF',
                    'target-arrow-shape': 'triangle',
                }
            }
        ]
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)