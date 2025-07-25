

import csv
import random
import os
import sys
import mailbox

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, 'emails.csv')
    output_dir = os.path.join(script_dir, 'email_samples')
    os.makedirs(output_dir, exist_ok=True)
    total_samples = 10000
    
    # 1. Get 10,000 unique samples
    all_samples = get_email_samples(csv_file, total_samples)
    
    if len(all_samples) == total_samples:
        # 2. Split the samples into two lists
        samples_1 = all_samples[:5000]
        samples_2 = all_samples[5000:]
        
        # 3. Create the two mbox files
        mbox_path_1 = os.path.join(output_dir, 'samples_1.mbox')
        create_mbox_from_messages(samples_1, mbox_path_1)
        
        mbox_path_2 = os.path.join(output_dir, 'samples_2.mbox')
        create_mbox_from_messages(samples_2, mbox_path_2)
        
        print("\nProcess complete.")
    else:
        print(f"\nProcess failed: Expected {total_samples} samples, but got {len(all_samples)}.")


