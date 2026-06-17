from datasets import load_dataset

ds = load_dataset("jslin09/wikipedia_tw", split="train")

titles = set()

for item in ds:
    t = item["title"]
    if t:
        titles.add(t.strip())

with open("wikipedia_titles.txt", "w", encoding="utf-8") as f:
    for t in sorted(titles):
        f.write(t + "\n")

print("done:", len(titles))