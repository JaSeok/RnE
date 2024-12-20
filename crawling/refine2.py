from typing import List

# Example function to score text blocks based on predefined criteria
def score_text_block(text_block: str) -> int:
    # Criteria for scoring
    length_score = len(text_block)  # Length of the text block
    keyword_score = 10 if any(keyword in text_block for keyword in ["특수임무", "대통령", "기자회견"]) else 0
    sentence_count = text_block.count(".")  # Sentence count in the block
    
    return length_score + keyword_score + (sentence_count * 5)

# Function to filter text based on scores
def filter_recognized_text(recognized_text: List[str]) -> List[str]:
    # Score each text block
    scored_texts = [(text, score_text_block(text)) for text in recognized_text]
    
    # Filter out low-scoring blocks (threshold can be adjusted)
    filtered_texts = [text for text, score in scored_texts if score > 50]
    return filtered_texts

# Function to remove duplicate lines while preserving order
def remove_duplicate_lines(text_lines: List[str]) -> List[str]:
    seen = set()  # To track unique lines
    unique_lines = []
    for line in text_lines:
        if line not in seen:  # Add only if not seen before
            seen.add(line)
            unique_lines.append(line)
    return unique_lines

# Function to load text from a file
def load_text_file(file_path: str) -> List[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]  # Remove empty lines
    except Exception as e:
        return []

# Function to save filtered text to a file
def save_filtered_text(filtered_text: List[str], output_file_path: str):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(filtered_text))

# Main function
def main():
    # Path to the text file
    file_path = "webpage_text.txt"  # Replace with your file path
    output_file_path = "webpage_text.txt"  # Path to save filtered text
    
    # Load recognized text from file
    recognized_text = load_text_file(file_path)
    
    # Remove duplicate lines while preserving order
    unique_text = remove_duplicate_lines(recognized_text)
    
    # Filter the recognized text
    filtered_text = filter_recognized_text(unique_text)
    
    # Save filtered text to file
    save_filtered_text(filtered_text, output_file_path)

if __name__ == "__main__":
    main()
