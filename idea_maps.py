import matplotlib.pyplot as plt
import json
import tkinter as tk
from tkinter import filedialog
import networkx as nx
from my_reingold import my_reingold
nx.drawing.layout._fruchterman_reingold = my_reingold


NUM_ROWS = 13
BOLD_FONT = ("calbri", 12, "bold")
NORMAL_FONT = ("calbri", 12, "normal")


def create_widgets():
    for i in range(NUM_ROWS):
        key = chr(i + 65)
        this_row = widgets[key] = {}
        this_row["label"] = tk.Label(root, text=key, font=BOLD_FONT)
        this_row["label"].grid(row=i, column=0, padx=5, pady=10)
        this_row["factor_field"] = tk.Entry(root, width=60, font=NORMAL_FONT)
        this_row["factor_field"].grid(row=i, column=1, padx=5, pady=10)
        this_row["target_node_field"] = tk.Entry(
            root, width=5, font=NORMAL_FONT)
        this_row["target_node_field"].grid(row=i, column=2, padx=5, pady=10)
        this_row["clear_button"] = tk.Button(root, text="Clear", command=lambda key=key: clear(
            key), font=BOLD_FONT).grid(row=i, column=3, padx=5, pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit,
                              font=BOLD_FONT).grid(row=NUM_ROWS + 1, column=0, padx=5, pady=10)
    save_button = tk.Button(root, text="Save", command=save,
                            font=BOLD_FONT).grid(row=NUM_ROWS + 1, column=1, padx=5, pady=10)
    load_button = tk.Button(root, text="Load", command=load,
                            font=BOLD_FONT).grid(row=NUM_ROWS + 1, column=2, padx=5, pady=10)


def validate_fields():
    legal_targets = list(widgets.keys()) + [""]  # to allow empty fields

    for key, row in widgets.items():
        factor_field_contents = row["factor_field"].get()
        target_node_field_contents = row["target_node_field"].get().upper()

        # Every target must belong to the set of available factors
        if target_node_field_contents not in legal_targets:
            return False

        #  Target factor field must not be empty
        if target_node_field_contents:
            if not widgets[target_node_field_contents]["factor_field"].get():
                return False

        # Every non-empty factor must have a target
        flen0 = len(factor_field_contents) == 0
        tlen0 = len(target_node_field_contents) == 0
        if (flen0 and not tlen0) or (not flen0 and tlen0):
            return False

    return True


def submit():
    plt.close()
    if validate_fields():
        G = nx.DiGraph()
        edges = []
        for key, row in widgets.items():
            factor_field_contents = row["factor_field"].get()
            target_node_field_contents = row["target_node_field"].get().upper()
            if factor_field_contents != "" and target_node_field_contents != "":
                edges.append((key, target_node_field_contents))
                data[key] = {"factor": factor_field_contents,
                             "target_node": target_node_field_contents}
        G.add_edges_from(edges)
        # pos = nx.spring_layout(G, k=1.0, iterations=50)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color="green")
        nx.draw_networkx_labels(G, pos, font_color="white")
        nx.draw_networkx_edges(
            G, pos, connectionstyle='arc3, rad = 0.1', width=2, arrows=True)
        plt.show()


def save():
    print("Attempting to save.")
    # print(f"data: {data}")
    if data:
        try:
            filename = filedialog.asksaveasfile(mode='w')
            json_data = json.dumps(data, indent=4)
            filename.write(json_data)
            print("Data saved.")
        except OSError as e:
            print(e)


def load():
    for key, entries in widgets.items():
        entries["factor_field"].delete(0, "end")
        entries["target_node_field"].delete(0, "end")
    try:
        filename = filedialog.askopenfile(mode='r')
        loaded_data = json.loads(filename.read())
        # print(loaded_data)
        for key, entries in loaded_data.items():
            widgets[key]["factor_field"].insert(0, entries["factor"])
            widgets[key]["target_node_field"].insert(0, entries["target_node"])
    except OSError as e:
        print(e)


def clear(key):
    widgets[key]["factor_field"].delete(0, "end")
    widgets[key]["target_node_field"].delete(0, "end")


if __name__ == "__main__":
    data = {}
    widgets = {}
    root = tk.Tk()
    root.title("Directional Idea Map")
    create_widgets()
    root.mainloop()
