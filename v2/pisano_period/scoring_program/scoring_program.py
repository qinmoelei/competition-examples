import json
# read output directory for memory, cpu, etc.
# generate a score somehow

# submit:
#     - generated score from all scores
#     - memory
#     - cpu
#     - character count


print("I should be seeing the ingestion program output crap in ./result")

char_count = 0

with open("input/solution.py", "r") as f:
    for c in f.read():
        char_count += 1




scores = json.loads(open("input/ingestion_results.json", "r").read())
# We should now have ingestion_output["mem"] and ingestion_output["cpu"]


scores["char_count"] = char_count




# We need to write to /app/output/scores.json with our leaderboard columns and such
with open("/app/output/scores.json", "w") as f:
    print(f"Writing scores... {scores}")
    f.write(json.dumps(scores))

