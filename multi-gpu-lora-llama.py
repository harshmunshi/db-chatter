import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import LlamaTokenizer, LlamaForCausalLM
from datasets import load_dataset
from peft import get_peft_model, LoraConfig
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.distributed as dist
from torch.utils.data.distributed import DistributedSampler

# GLOBALS
n_epochs = 10

def setup(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup():
    dist.destroy_process_group()

def main(rank, world_size):
    setup(rank, world_size)

    # Load tokenizer and dataset
    tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-3.3-7B")
    dataset = load_dataset("json", data_files="data.json")
    train_data = dataset["train"]

    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

    train_data = train_data.map(tokenize_function, batched=True)
    train_data.set_format(type="torch", columns=["input_ids", "attention_mask"])

    # Create DataLoader
    train_sampler = DistributedSampler(train_data, num_replicas=world_size, rank=rank)
    train_loader = DataLoader(train_data, batch_size=8, sampler=train_sampler)

    # Load model
    model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-3.3-7B", torch_dtype=torch.float16)
    model = model.to(rank)

    # Apply LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    # Wrap model with DDP
    model = DDP(model, device_ids=[rank])

    # Define optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

    # Training loop
    model.train()
    for epoch in range(n_epochs):
        train_sampler.set_epoch(epoch)
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(rank)
            attention_mask = batch["attention_mask"].to(rank)
            labels = input_ids.clone()

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            if rank == 0:
                print(f"Epoch {epoch}, Loss: {loss.item()}")

    cleanup()

if __name__ == "__main__":
    world_size = 4
    torch.multiprocessing.spawn(main, args=(world_size,), nprocs=world_size, join=True)