import os

def list_tree(start_path, indent=""):
    for item in os.listdir(start_path):
        path = os.path.join(start_path, item)
        print(indent + item)
        if os.path.isdir(path):
            list_tree(path, indent + "    ")

if __name__ == "__main__":
    print("PROJECT STRUCTURE:\n")
    list_tree(".")
