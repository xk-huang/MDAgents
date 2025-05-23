import dotenv

dotenv.load_dotenv(override=True)

import argparse
import json
import os
import random

from pptree import print_tree
from prettytable import PrettyTable
from termcolor import cprint
from tqdm import tqdm

from utils import (
    Agent,
    Group,
    create_question,
    determine_difficulty,
    load_data,
    parse_group_info,
    parse_hierarchy,
    process_advanced_query,
    process_basic_query,
    process_intermediate_query,
    setup_model,
)

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="medqa")
parser.add_argument("--model", type=str, default="gpt-4o-mini")
parser.add_argument("--difficulty", type=str, default="adaptive")
parser.add_argument("--num_samples", type=int, default=50)
args = parser.parse_args()

# model, client = setup_model(args.model)
test_qa, examplers = load_data(args.dataset)

agent_emoji = [
    "\U0001f468\u200d\u2695\ufe0f",
    "\U0001f468\U0001f3fb\u200d\u2695\ufe0f",
    "\U0001f469\U0001f3fc\u200d\u2695\ufe0f",
    "\U0001f469\U0001f3fb\u200d\u2695\ufe0f",
    "\U0001f9d1\u200d\u2695\ufe0f",
    "\U0001f9d1\U0001f3ff\u200d\u2695\ufe0f",
    "\U0001f468\U0001f3ff\u200d\u2695\ufe0f",
    "\U0001f468\U0001f3fd\u200d\u2695\ufe0f",
    "\U0001f9d1\U0001f3fd\u200d\u2695\ufe0f",
    "\U0001f468\U0001f3fd\u200d\u2695\ufe0f",
]
random.shuffle(agent_emoji)

print(f"num_samples: {args.num_samples}")
results = []
for no, sample in enumerate(tqdm(test_qa)):
    if no == args.num_samples:
        break

    print(f"\n[INFO] no: {no}")
    total_api_calls = 0

    question, img_path = create_question(sample, args.dataset)
    difficulty = determine_difficulty(question, args.difficulty)

    print(f"difficulty: {difficulty}")

    if difficulty == "basic":
        final_decision = process_basic_query(question, examplers, args.model, args)
    elif difficulty == "intermediate":
        final_decision = process_intermediate_query(
            question, examplers, args.model, args
        )
    elif difficulty == "advanced":
        final_decision = process_advanced_query(question, args.model, args)

    if args.dataset == "medqa":
        results.append(
            {
                "question": question,
                "label": sample["answer_idx"],
                "answer": sample["answer"],
                "options": sample["options"],
                "response": final_decision,
                "difficulty": difficulty,
            }
        )

# Save results
path = os.path.join(os.getcwd(), "output")
if not os.path.exists(path):
    os.makedirs(path)

with open(f"output/{args.model}_{args.dataset}_{args.difficulty}.json", "w") as file:
    json.dump(results, file, indent=4)
