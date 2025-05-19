import os

def explore_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"Directory: {dirpath}")
        for dirname in dirnames:
            print(f"  [Folder] {dirname}")
        for filename in filenames:
            print(f"  [File] {filename}")

if __name__ == "__main__":
    root = r"D:\ATE_Operator_Helper\ATE_Operator_Helper\dist"  # Use raw string for Windows path
    explore_directory(root)
