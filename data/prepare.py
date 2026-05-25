from datasets import load_dataset
import json

print("Downloading IMDB dataset...")
dataset = load_dataset("imdb")

data = {
    "train": {
        "texts": dataset["train"]["text"],
        "labels": dataset["train"]["label"]
    },
    "test": {
        "texts": dataset["test"]["text"],
        "labels": dataset["test"]["label"]
    }
}

with open("data/imdb.json", "w") as f:
    json.dump(data, f)

print(f"Saved {len(data['train']['texts'])} training samples")
print(f"Saved {len(data['test']['texts'])} test samples")
