import json
import random
from datetime import datetime
from faker import Faker

fake = Faker()

# Configuration
NUM_COMMUNITIES = 20
RELATIONSHIPS_PER_COMMUNITY = 50
MIN_USERS = 60
MAX_USERS = 100  # 👈 Max users per community is now capped at 100

def generate_community_id(index):
    return int(f"999999999999{index:04}")

def generate_user_node(community_id, user_id):
    return {
        "id": str(user_id),
        "entityType": "node",
        "labels": "user",
        "community": community_id,
        "country": "Canada",
        "city": fake.city(),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d"),
        "state": fake.state(),
        "plan_start_dt": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d")
    }

nodes_data = {}
communities_data = {}
relationships_data = {}
user_ids_by_community = {}

global_user_id = 4001000000

for c in range(NUM_COMMUNITIES):
    community_id = generate_community_id(c)
    community_size = random.randint(MIN_USERS, MAX_USERS)  # 👈 Random between 60–100
    users = []
    user_ids = []

    for _ in range(community_size):
        user_id = global_user_id
        global_user_id += 1
        users.append(generate_user_node(community_id, user_id))
        user_ids.append(str(user_id))

    nodes_data[str(community_id)] = {"nodes": users}
    communities_data[str(community_id)] = {
        "size": community_size,
        "community": community_id
    }
    user_ids_by_community[community_id] = user_ids

for community_id, user_ids in user_ids_by_community.items():
    links = []
    max_possible_links = len(user_ids) * (len(user_ids) - 1) // 2
    actual_links = min(RELATIONSHIPS_PER_COMMUNITY, max_possible_links)

    for _ in range(actual_links):
        from_user, to_user = random.sample(user_ids, 2)
        links.append({"from": from_user, "to": to_user})

    relationships_data[str(community_id)] = {str(community_id): links}

# Save files
with open("nodes.json", "w") as f:
    json.dump(nodes_data, f, indent=2)

with open("communities.json", "w") as f:
    json.dump(communities_data, f, indent=2)

with open("relationships.json", "w") as f:
    json.dump(relationships_data, f, indent=2)

print("✔ All files saved: nodes.json, communities.json, relationships.json")
