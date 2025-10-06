import heapq
import re

# ------------------------------------------------------------
# Step 1: Text Preprocessing (Normalization and Sentence Tokenization)
# ------------------------------------------------------------
def preprocess_document(text):
    """
    Normalize and split the text into clean, lowercase sentences.
    """
    # Convert to lowercase for consistency
    text = text.lower()
    
    # Replace newlines with periods to maintain sentence boundaries
    text = text.replace('\n', '.')
    
    # Remove punctuation except sentence-ending periods
    text = re.sub(r'[^\w\s\.]', '', text)
    
    # Split text into sentences
    sentences = text.split('.')
    
    # Clean and filter out empty sentences
    cleaned_sentences = [s.strip() for s in sentences if s.strip()]

    # Display preprocessed sentences for verification
    print("Processed Sentences:\n")
    for idx, sentence in enumerate(cleaned_sentences, start=1):
        print(f"Sentence {idx}: {sentence}")
    print("\n")

    return cleaned_sentences


# ------------------------------------------------------------
# Step 2: Levenshtein Edit Distance Calculation
# ------------------------------------------------------------
def compute_edit_distance(str1, str2):
    """
    Compute the Levenshtein distance (edit distance) between two strings.
    """
    dp = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]

    for i in range(len(str1) + 1):
        for j in range(len(str2) + 1):
            if i == 0:
                dp[i][j] = j  # All insertions
            elif j == 0:
                dp[i][j] = i  # All deletions
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[-1][-1]


# ------------------------------------------------------------
# Step 3: A* Node Class
# ------------------------------------------------------------
class AlignmentNode:
    def __init__(self, idx1, idx2, cost_so_far, heuristic_cost, parent=None):
        self.idx1 = idx1
        self.idx2 = idx2
        self.cost_so_far = cost_so_far
        self.heuristic_cost = heuristic_cost
        self.parent = parent

    def total_cost(self):
        return self.cost_so_far + self.heuristic_cost

    def __lt__(self, other):
        return self.total_cost() < other.total_cost()


# ------------------------------------------------------------
# Step 4: Heuristic Function for A* Search
# ------------------------------------------------------------
def estimate_remaining_cost(idx1, idx2, sentences1, sentences2):
    """
    Estimate remaining cost using the number of unaligned sentences.
    """
    remaining1 = len(sentences1) - idx1
    remaining2 = len(sentences2) - idx2

    if remaining1 == 0 or remaining2 == 0:
        # Penalize unaligned remaining sentences
        return max(remaining1, remaining2) * 10
    return (remaining1 + remaining2) / 2


# ------------------------------------------------------------
# Step 5: A* Search for Sentence Alignment
# ------------------------------------------------------------
def perform_astar_alignment(sentences1, sentences2):
    """
    Use A* search to align sentences between two documents.
    """
    start_node = AlignmentNode(0, 0, 0, estimate_remaining_cost(0, 0, sentences1, sentences2))
    frontier = []
    heapq.heappush(frontier, start_node)
    explored = set()

    while frontier:
        current = heapq.heappop(frontier)
        idx1, idx2 = current.idx1, current.idx2

        print(f"Exploring: Doc1={idx1}, Doc2={idx2}, g={current.cost_so_far}, h={current.heuristic_cost}")

        # Goal: both documents fully processed
        if idx1 == len(sentences1) and idx2 == len(sentences2):
            path = []
            node = current
            while node:
                path.append((node.idx1, node.idx2))
                node = node.parent
            return path[::-1]

        explored.add((idx1, idx2))

        # Possible moves: align (1,1), skip doc1 (1,0), skip doc2 (0,1)
        for move in [(1, 1), (1, 0), (0, 1)]:
            new_idx1, new_idx2 = idx1 + move[0], idx2 + move[1]

            if new_idx1 <= len(sentences1) and new_idx2 <= len(sentences2) and (new_idx1, new_idx2) not in explored:
                new_cost = current.cost_so_far

                if move == (1, 1):
                    # Align two sentences
                    new_cost += compute_edit_distance(sentences1[idx1], sentences2[idx2])
                else:
                    # Skip penalty
                    new_cost += 1

                heuristic_cost = estimate_remaining_cost(new_idx1, new_idx2, sentences1, sentences2)
                next_node = AlignmentNode(new_idx1, new_idx2, new_cost, heuristic_cost, current)
                heapq.heappush(frontier, next_node)

    return None


# ------------------------------------------------------------
# Step 6: Document Alignment Wrapper
# ------------------------------------------------------------
def align_documents(doc_text1, doc_text2):
    """
    Align two documents at the sentence level using A*.
    """
    sentences1 = preprocess_document(doc_text1)
    sentences2 = preprocess_document(doc_text2)

    alignment_path = perform_astar_alignment(sentences1, sentences2)

    aligned_pairs = []
    for i, j in alignment_path:
        if i < len(sentences1) and j < len(sentences2):
            distance = compute_edit_distance(sentences1[i], sentences2[j])
            aligned_pairs.append((sentences1[i], sentences2[j], distance))
        elif i < len(sentences1):
            aligned_pairs.append((sentences1[i], None, None))
        elif j < len(sentences2):
            aligned_pairs.append((None, sentences2[j], None))

    return aligned_pairs


# ------------------------------------------------------------
# Step 7: Plagiarism Detection
# ------------------------------------------------------------
def identify_plagiarized_pairs(aligned_pairs, distance_threshold=5, similarity_threshold=0.7):
    """
    Detect potentially plagiarized sentence pairs using edit distance and similarity.
    """
    plagiarized_matches = []

    for s1, s2, distance in aligned_pairs:
        if s1 and s2 and distance is not None:
            max_len = max(len(s1), len(s2))
            similarity_score = 1 - (distance / max_len)

            if distance <= distance_threshold or similarity_score >= similarity_threshold:
                plagiarized_matches.append((s1, s2, distance, similarity_score))

    return plagiarized_matches


# ------------------------------------------------------------
# Step 8: File Handling Utilities
# ------------------------------------------------------------
def read_text_file(path):
    with open(path, 'r') as file:
        return file.read()


# ------------------------------------------------------------
# Step 9: Main Pipeline Execution
# ------------------------------------------------------------
def run_plagiarism_detection(file1_path, file2_path, output_path):
    doc_text1 = read_text_file(file1_path)
    doc_text2 = read_text_file(file2_path)

    aligned_results = align_documents(doc_text1, doc_text2)

    with open(output_path, 'a') as out_file:
        out_file.write("Sentence Alignment with Edit Distances:\n\n")
        for s1, s2, dist in aligned_results:
            if s1 is None:
                out_file.write(f"Doc1: [Missing]\nDoc2: {s2}\n\n")
            elif s2 is None:
                out_file.write(f"Doc1: {s1}\nDoc2: [Missing]\n\n")
            else:
                out_file.write(f"Doc1: {s1}\nDoc2: {s2}\nEdit Distance: {dist}\n\n")

        # Run plagiarism detection
        suspicious_pairs = identify_plagiarized_pairs(aligned_results)

        out_file.write("\nDetected Potential Plagiarism:\n\n")
        for s1, s2, dist, sim in suspicious_pairs:
            out_file.write(
                f"Sentence 1: {s1}\nSentence 2: {s2}\nEdit Distance: {dist}\nSimilarity: {sim:.2f}\n\n"
            )

    print("Analysis complete. Results written to file.")


# ------------------------------------------------------------
# Step 10: Example Usage
# ------------------------------------------------------------
if __name__ == "__main__":
    file1_path = "doc1.txt"
    file2_path = "doc2.txt"
    output_path = "alignment_results.txt"

    run_plagiarism_detection(file1_path, file2_path, output_path)
