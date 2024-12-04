import xml.etree.ElementTree as ET


# Function to sanitize and normalize text
def sanitize_text(text):
    if text:
        return " ".join(text.split())  # Replace newlines and multiple spaces with a single space
    return ""


# Updated script to handle newlines in fields
def xml_to_markdown(input_xml, output_md):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    namespace = {"ns": "http://uima.apache.org/resourceSpecifier"}  # Add namespace if needed
    types = root.findall(".//ns:typeDescription", namespace)

    with open(output_md, "w") as md_file:
        for type_desc in types:
            name = type_desc.find("ns:name", namespace).text
            description = sanitize_text(type_desc.find("ns:description", namespace).text or "")
            supertype = type_desc.find("ns:supertypeName", namespace).text.split(".")[-1]

            # Write header information
            md_file.write(f"### {name.split('.')[-1].replace('Token', '').strip()}\n\n")
            md_file.write(f"<details>\n<summary>{description}</summary>\n\n")
            md_file.write(f"**Parent Name:** {supertype}\n\n")

            # Process features
            features = type_desc.findall(".//ns:featureDescription", namespace)
            if features:
                md_file.write("| Feature Name | Description | Type | Element Type |\n")
                md_file.write("| --- | --- | --- | --- |\n")
                for feature in features:
                    feature_name = sanitize_text(feature.find("ns:name", namespace).text or "")
                    feature_description = sanitize_text(feature.find("ns:description", namespace).text or "")
                    range_type = sanitize_text(feature.find("ns:rangeTypeName", namespace).text or "")
                    element_type_node = feature.find("ns:elementType", namespace)
                    element_type = sanitize_text(
                        element_type_node.text.split(".")[-1] if element_type_node is not None else "")

                    # Add data to the table row
                    md_file.write(f"| {feature_name} | {feature_description} | {range_type} | {element_type} |\n")
            else:
                md_file.write("No <features> found in this section.\n\n")

            md_file.write("</details>\n\n")


# Replace with your XML input and Markdown output file paths
input_xml = "TypeSystem.xml"
output_md = "testOutput.md"

xml_to_markdown(input_xml, output_md)
