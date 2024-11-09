import json

def remove_duplicates_by_id(input_file, output_file):
    # Dictionary to store unique entries
    unique_entries = {}
    
    # Read the input file and process each line
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Parse JSON object from line
                entry = json.loads(line.strip())
                # Store entry using id as key (this automatically overwrites duplicates)
                unique_entries[entry['id']] = entry
            except json.JSONDecodeError:
                # Skip lines that aren't valid JSON (like the omitted lines indicator)
                continue
    
    # Write unique entries to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in unique_entries.values():
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')
    
    # Return some statistics
    return {
        'total_processed': len(unique_entries),
        'duplicates_removed': len(unique_entries)
    }

# # Remove duplicates from the dataset
# dataset_input_file = 'dataset/data.jsonl'
# dataset_output_file = 'dataset/rm_dup_data.jsonl'
# stats = remove_duplicates_by_id(dataset_input_file, dataset_output_file)
# print(f"Processed {stats['total_processed']} unique entries from dataset")

# # Remove duplicates from the results
# perplexity_input_file = 'results/perplexity_ai_results.jsonl'
# perplexity_output_file = 'results/cleaned/rm_dup_perplexity_ai_results.jsonl'
# stats = remove_duplicates_by_id(perplexity_input_file, perplexity_output_file)
# print(f"Processed {stats['total_processed']} unique entries from perplexity results")

# # Remove duplicates from You.com results
# you_input_file = 'results/you_results.jsonl'
# you_output_file = 'results/cleaned/rm_dup_you_results.jsonl'
# stats = remove_duplicates_by_id(you_input_file, you_output_file)
# print(f"Processed {stats['total_processed']} unique entries from You.com results")

# # Remove duplicates from Andi search results
# andi_input_file = 'results/andi_search_result.jsonl'
# andi_output_file = 'results/cleaned/rm_dup_andi_search_result.jsonl'
# stats = remove_duplicates_by_id(andi_input_file, andi_output_file)
# print(f"Processed {stats['total_processed']} unique entries from Andi search results")

def validate_results(dataset_file, result_file, unused_output_file=None):
    """
    Validate results against dataset and check for missing or unused entries
    
    Args:
        dataset_file: Path to the cleaned dataset file
        result_file: Path to the cleaned results file
        unused_output_file: Optional path to save unused results
        
    Returns:
        dict: Statistics about the validation process
    """
    dataset_entries = {}
    result_entries = {}
    unused_results = []
    missing_ids = []

    # Load dataset entries
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            dataset_entries[entry['id']] = entry['question']

    # Load and check result entries
    with open(result_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            result_entries[entry['id']] = entry
            
            # Check if this result entry corresponds to a dataset entry
            if entry['id'] not in dataset_entries:
                unused_results.append(entry)
            elif entry['question'] != dataset_entries[entry['id']]:
                print(f"Warning: Question mismatch for ID {entry['id']}")
                print(f"Dataset: {dataset_entries[entry['id']]}")
                print(f"Result:  {entry['question']}")

    # Find missing dataset entries
    for dataset_id in dataset_entries:
        if dataset_id not in result_entries:
            missing_ids.append(dataset_id)

    # Save unused results if there are any and output file is specified
    if unused_results and unused_output_file:
        with open(unused_output_file, 'w', encoding='utf-8') as f:
            for entry in unused_results:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')

    # Prepare statistics
    stats = {
        'total_dataset_entries': len(dataset_entries),
        'total_result_entries': len(result_entries),
        'missing_entries': len(missing_ids),
        'unused_results': len(unused_results),
        'missing_ids': missing_ids
    }

    return stats

# Example usage for each result file
def validate_all_results():
    dataset_file = 'dataset/rm_dup_data.jsonl'
    result_files = {
        'perplexity': 'results/cleaned/rm_dup_perplexity_ai_results.jsonl',
        'you': 'results/cleaned/rm_dup_you_results.jsonl',
        'andi': 'results/cleaned/rm_dup_andi_search_result.jsonl'
    }

    for source, result_file in result_files.items():
        print(f"\nValidating {source} results...")
        unused_output = f'results/cleaned/unused_{source}_results.jsonl'
        stats = validate_results(dataset_file, result_file, unused_output)
        
        print(f"Dataset entries: {stats['total_dataset_entries']}")
        print(f"Result entries: {stats['total_result_entries']}")
        print(f"Missing entries: {stats['missing_entries']}")
        print(f"Unused results: {stats['unused_results']}")
        
        if stats['missing_entries'] > 0:
            print(f"Missing IDs: {stats['missing_ids']}")

# # Run the validation
# if __name__ == "__main__":
#     validate_all_results()