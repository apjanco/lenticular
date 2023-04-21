from datasets import load_dataset

dataset = load_dataset("stevhliu/demo")
dataset.push_to_hub("stevhliu/processed_demo")