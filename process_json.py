import json
import os
import sys
import xml.etree.ElementTree as ET
sys.path.append("../")

def extract_document_id(xml_file):
    doc_id = os.path.splitext(os.path.split(xml_file)[-1])
    extracted_part = doc_id[0].split(".")[0]
    return extracted_part


def extract_original_text(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Find all elements with the tag 'ORIGINAL_TEXT'
    original_text_elements = root.findall(".//ORIGINAL_TEXT")
    # Combine the text content into a single string
    combined_text = " ".join(element.text for element in original_text_elements)
    return combined_text

def is_document_id_present(json_file_path, document_id):
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
        print(json_data)
        
        for line in file:
            print(line)
            try:
                json_data = json.loads(line)
                # print(json_data)
                documents = json_data["documents"]
                print(len(documents))
            
                for item in documents:
                    if item[0] == document_id and item[1] == 1:
                        return True
                    else:
                        return False
            except json.JSONDecodeError:
                pass  # Ignore lines that are not valid JSON

    return False

def process_xml_files(folder_path, output_path):
    context_folder = folder_path + "ltf/"
    train_label_path = folder_path + "split.train.json"
    test_label_path = folder_path + "split.test.json"
    valid_label_path = folder_path + "split.valid.json"

    path_components = context_folder.split(os.path.sep)
    # Get the list of all .xml files in the folder
    xml_files = [f for f in os.listdir(context_folder) if f.endswith(".xml")]
    count = 1

    # Iterate through each XML file
    for xml_file in xml_files:
        # Get the full path of the XML file
        xml_file_path = os.path.join(context_folder, xml_file)
        # Extract original text from the XML file
        original_text = extract_original_text(xml_file_path)
        document_id = extract_document_id(xml_file_path)

        if is_document_id_present(train_label_path, document_id) or is_document_id_present(test_label_path, document_id) or is_document_id_present(valid_label_path, document_id):
            tail = "TRUE"
        else: 
            tail = "FALSE"
        # Print or do something with the extracted text
        # print(f"File: {xml_file}")
        # print("Original Text:", original_text)
        txt_file_path = os.path.join(output_path, f"{path_components[2]}{count}{tail}.txt")
        
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(original_text)
        count += 1
    print(count)

# Specify the folder path you want to explore
folder_path = "./data/Crisis/"
output_path = "./original_text"

os.makedirs(output_path, exist_ok=True)
process_xml_files(folder_path, output_path)

