import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from datetime import datetime


def replace_characters(text):
    replacements = {
        '/': '.',
        '\\': '.',
        'º': 'o',
        'ª': 'a',
        'ñ': 'n',
        'ç': 'c',
        'Ñ': 'N',
        'Ç': 'C'
    }
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)
    return text


def getparent(element, tree):
    for parent in tree.iter():
        if element in list(parent):
            return parent
    return None


def process_xml_file(path):
    ET.register_namespace('', 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03')
    tree = ET.parse(path)
    root = tree.getroot()

    first_id_modified = False

    for elem in root.iter():
        if elem.text:
            elem.text = replace_characters(elem.text)
        if elem.tail:
            elem.tail = replace_characters(elem.tail)
        parent = getparent(elem, tree)
        if elem.tag.endswith('Id') and parent is not None and parent.tag.endswith('Othr'):
            if not first_id_modified:
                elem.text += 'T00'
                first_id_modified = True

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_path = path.replace('.xml', f'_{timestamp}.xml')
    try:
        tree.write(new_path, encoding='utf-8', xml_declaration=True, method="xml")
        messagebox.showinfo("Proceso terminado", f"Archivo procesado y guardado como: {new_path}")
    except Exception as e:
        messagebox.showerror("Proceso con error", f"Error al guardar el archivo: {e}")


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        process_xml_file(file_path)
        root.mainloop()


if __name__ == "__main__":
    open_file_dialog()
