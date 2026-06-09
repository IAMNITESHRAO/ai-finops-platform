from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()

providers = [
    ("OpenAI", 45),
    ("Claude", 30),
    ("Gemini", 15),
    ("DeepSeek", 10)
]

provider = random.choices(
    [p[0] for p in providers],
    weights=[p[1] for p in providers],
    k=1
)[0]

teams = [
    "Engineering",
    "Security",
    "Finance",
    "Operations",
    "Marketing"
]

records = []

for _ in range(1000000):

    provider = random.choice(list(providers.keys()))
    model = random.choice(providers[provider])

    input_tokens = random.randint(100, 5000)
    output_tokens = random.randint(50, 3000)

    total_tokens = input_tokens + output_tokens

    cost = round(total_tokens * 0.00002, 4)

    records.append({
        "timestamp": fake.date_time_this_year(),
        "provider": provider,
        "model": model,
        "team": random.choice(teams),
        "user": fake.user_name(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost
    })

df = pd.DataFrame(records)

df.to_parquet(
    "data-lake/bronze/ai_usage.parquet",
    index=False
)

df.to_csv(
    "data-generator/ai_usage_data.csv",
    index=False
)

print("Generated:", len(df))
print(df.head())

# THIS CODE SHOWS OUTPUT IN THE TERMINAL

# from faker import Faker
# import pandas as pd
# import random
# import json
# from pathlib import Path

# fake = Faker()

# providers = {
#     "OpenAI": ["gpt-4o", "gpt-4.1-mini"],
#     "Claude": ["claude-sonnet", "claude-opus"],
#     "Gemini": ["gemini-2.5-pro", "gemini-flash"],
#     "DeepSeek": ["deepseek-chat", "deepseek-reasoner"]
# }

# teams = [
#     "Engineering",
#     "Security",
#     "Finance",
#     "Operations",
#     "Marketing"
# ]

# records = []

# for _ in range(10000):

#     provider = random.choice(list(providers.keys()))
#     model = random.choice(providers[provider])

#     input_tokens = random.randint(100, 5000)
#     output_tokens = random.randint(50, 3000)

#     total_tokens = input_tokens + output_tokens

#     cost = round(total_tokens * 0.00002, 4)

#     record = {
#         "timestamp": str(fake.date_time_this_year()),
#         "provider": provider,
#         "model": model,
#         "team": random.choice(teams),
#         "user": fake.user_name(),
#         "input_tokens": input_tokens,
#         "output_tokens": output_tokens,
#         "total_tokens": total_tokens,
#         "cost_usd": cost
#     }

#     records.append(record)

# # Print first 20 records as JSON
# print("\n===== SAMPLE JSON RECORDS =====\n")

# for record in records[:20]:
#     print(json.dumps(record, indent=2))

# # Create DataFrame
# df = pd.DataFrame(records)

# print("\n===== DATAFRAME PREVIEW =====\n")
# print(df.head())

# print("\n===== DATAFRAME INFO =====\n")
# print(df.info())

# print("\n===== DATAFRAME SHAPE =====\n")
# print(df.shape)

# # Create output directory if not exists
# BASE_DIR = Path(__file__).resolve().parent.parent
# BRONZE_DIR = BASE_DIR / "data-lake" / "bronze"

# BRONZE_DIR.mkdir(parents=True, exist_ok=True)

# # Save parquet file
# output_file = BRONZE_DIR / "ai_usage.parquet"

# df.to_parquet(
#     output_file,
#     index=False
# )

# print(f"\nParquet file saved at: {output_file}")
# print(f"Generated {len(df)} records successfully.")