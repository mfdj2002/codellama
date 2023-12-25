# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import Optional

import fire

from llama import Llama


import os
import select
import time

def main(
        
    #TODO: queue for intercommunication

    ckpt_dir: str, #TODO: add default dir
    tokenizer_path: str, ##TODO: add default dir
    temperature: float = 0.2,
    top_p: float = 0.95,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    cache = {}

    instructions = [
        [
            {
                "role": "user",
                "content": "In Bash, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month?",
            }
        ],
        [
            {
                "role": "user",
                "content": "What is the difference between inorder and preorder traversal? Give an example in Python.",
            }
        ],
        [
            {
                "role": "system",
                "content": "Provide answers in JavaScript",
            },
            {
                "role": "user",
                "content": "Write a function that computes the set of sums of all contiguous sublists of a given list.",
            }
        ],
    ]

#pipe for intercommunication
IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"

def get_message(fifo):
    '''Read n bytes from pipe. Note: n=24 is an example'''
    return os.read(fifo, 24)

def process_msg(msg):
    '''Process message read from pipe'''
    return msg

    results = generator.chat_completion(
        instructions,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    for instruction, result in zip(instructions, results):
        for msg in instruction:
            cache[...] = msg["content"] #fn name or the whole hierarchy
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")
        print(
            f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        )
        print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)

    
    #python pipe execution
    os.mkfifo(IPC_FIFO_NAME_A)  # Create Pipe A
    os.mkfifo(IPC_FIFO_NAME_B)  # Create Pipe B

    try:
        fifo_a = os.open(IPC_FIFO_NAME_A, os.O_RDONLY)  # Pipe A is opened as read-only
        print('Pipe A ready')

        while True:
            try:
                fifo_b = os.open(IPC_FIFO_NAME_B, os.O_WRONLY)
                print("Pipe B ready")
                break
            except:
                # Wait until Pipe B has been initialized
                time.sleep(1)

        try:
            poll = select.poll()
            poll.register(fifo_a, select.POLLIN)

            try:
                while True:
                    if (fifo_a, select.POLLIN) in poll.poll(1000):  # Poll every 1 sec
                        msg = get_message(fifo_a)                   # Read from Pipe A
                        msg = process_msg(msg)                      # Process Message
                        os.write(fifo_b, msg)                       # Write to Pipe B

                        print('----- Received from JS -----')
                        print("    " + msg.decode("utf-8"))
            finally:
                poll.unregister(fifo_a)
        finally:
            os.close(fifo_a)
    finally:
        os.remove(IPC_FIFO_NAME_A)
        os.remove(IPC_FIFO_NAME_B)

