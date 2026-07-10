from persistant import initial_add_data

print("=== TEST 1: Initial Add Data ===")
file_path = r"C:\Users\faroz\OneDrive\Documents\GenAI\Chat_APP - RAG - chroma\data\tirukkural_output.txt"
uuids = initial_add_data(file_path)
print(f"Total UUIDs created: {len(uuids)}")
print(f"First 3 UUIDs: {uuids[:3]}")
print()