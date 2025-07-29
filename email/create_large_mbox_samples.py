

import csv
import random
import os
import sys
import mailbox
import argparse
import numpy as np

def set_csv_field_size_limit():
    """Sets the CSV field size limit to the maximum possible value."""
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int / 2)

def get_email_samples(csv_path, num_samples):
    """
    Uses reservoir sampling to select a random sample of email messages
    from a large CSV file.
    """
    set_csv_field_size_limit()

    reservoir = []
    message_col_index = -1

    print("Step 1: Finding 'message' column...")
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
            if 'message' in header:
                message_col_index = header.index('message')
            else:
                print("Error: 'message' column not found in CSV header.")
                return []
        except StopIteration:
            print("Error: CSV file is empty.")
            return []

    print(f"Step 2: Performing reservoir sampling for {num_samples} emails. This will take a while...")
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for i, row in enumerate(reader):
            if (i + 1) % 50000 == 0:
                print(f"  ...processed {i + 1} rows...")

            if len(row) <= message_col_index:
                continue # Skip malformed rows

            if i < num_samples:
                reservoir.append(row[message_col_index])
            else:
                j = random.randint(0, i)
                if j < num_samples:
                    reservoir[j] = row[message_col_index]

    print(f"Sampling complete. Acquired {len(reservoir)} samples.")
    return reservoir

def create_mbox_from_messages(messages, mbox_path):
    """
    Creates a single .mbox file from a list of email message strings.
    """
    print(f"Creating mbox file at {mbox_path}...")
    mb = mailbox.mbox(mbox_path)
    mb.lock()

    try:
        for msg_content in messages:
            # The content from the CSV is a full email, so we can add it directly
            msg = mailbox.mboxMessage(msg_content.encode('utf-8', 'ignore'))
            mb.add(msg)
        print(f"Successfully added {len(messages)} emails to {mbox_path}")
    finally:
        mb.flush()
        mb.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create large mbox samples from a CSV file.")
    parser.add_argument("--num-samples", type=int, default=10000, help="Total number of email samples to extract.")
    parser.add_argument("--output-dir", default="email/email_samples", help="Directory to save the mbox files.")
    parser.add_argument("--num-mbox-files", type=int, default=2, help="Number of mbox files to create.")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, 'emails.csv')
    os.makedirs(args.output_dir, exist_ok=True)

    all_samples = get_email_samples(csv_file, args.num_samples)

    if len(all_samples) == args.num_samples:
        # Split the samples into chunks
        sample_chunks = np.array_split(all_samples, args.num_mbox_files)

        for i, chunk in enumerate(sample_chunks):
            mbox_path = os.path.join(args.output_dir, f'samples_{i+1}.mbox')
            create_mbox_from_messages(chunk.tolist(), mbox_path)

        print("\nProcess complete.")
    else:
        print(f"\nProcess failed: Expected {args.num_samples} samples, but got {len(all_samples)}.")


