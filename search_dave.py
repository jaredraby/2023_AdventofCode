#!/usr/bin/env python3
"""
Search for 'Dave is cool' in large documents using regex.
Handles files with millions of pages efficiently using streaming.
"""

import re
import sys
import mmap
from pathlib import Path
import argparse
from typing import Iterator, Tuple

def search_phrase_in_file(filepath: str, phrase: str = "Dave is cool", 
                         case_sensitive: bool = True, 
                         chunk_size: int = 1024 * 1024) -> Iterator[Tuple[int, int, str]]:
    """
    Search for a phrase in a large file using memory-mapped I/O for efficiency.
    
    Args:
        filepath: Path to the file to search
        phrase: The phrase to search for (default: "Dave is cool")
        case_sensitive: Whether the search should be case-sensitive
        chunk_size: Size of chunks to read at a time (default: 1MB)
        
    Yields:
        Tuples of (line_number, position_in_line, matching_line)
    """
    # Compile regex pattern
    flags = 0 if case_sensitive else re.IGNORECASE
    # Escape special regex characters in the phrase
    escaped_phrase = re.escape(phrase)
    pattern = re.compile(escaped_phrase, flags)
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            line_number = 0
            
            for line in file:
                line_number += 1
                
                # Find all matches in the current line
                for match in pattern.finditer(line):
                    yield (line_number, match.start(), line.strip())
                    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def search_phrase_mmap(filepath: str, phrase: str = "Dave is cool",
                      case_sensitive: bool = True) -> Iterator[Tuple[int, int]]:
    """
    Alternative method using memory-mapped file for even better performance on huge files.
    
    Args:
        filepath: Path to the file to search
        phrase: The phrase to search for
        case_sensitive: Whether the search should be case-sensitive
        
    Yields:
        Tuples of (byte_position, line_number)
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    escaped_phrase = re.escape(phrase)
    pattern = re.compile(escaped_phrase.encode('utf-8'), flags)
    
    try:
        with open(filepath, 'rb') as file:
            # Memory-map the file for efficient access
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                line_number = 1
                last_newline_pos = -1
                
                # Search for all occurrences
                for match in pattern.finditer(mmapped_file):
                    pos = match.start()
                    
                    # Count line numbers up to this position
                    line_number = mmapped_file[:pos].count(b'\n') + 1
                    
                    yield (pos, line_number)
                    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def main():
    parser = argparse.ArgumentParser(
        description='Search for "Dave is cool" (or custom phrase) in large documents'
    )
    parser.add_argument('file', help='Path to the file to search')
    parser.add_argument('-p', '--phrase', default='Dave is cool',
                       help='Phrase to search for (default: "Dave is cool")')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                       help='Case-insensitive search')
    parser.add_argument('-c', '--count-only', action='store_true',
                       help='Only show the count of matches')
    parser.add_argument('-m', '--use-mmap', action='store_true',
                       help='Use memory-mapped file (faster for very large files)')
    parser.add_argument('-n', '--max-results', type=int, default=None,
                       help='Maximum number of results to show')
    
    args = parser.parse_args()
    
    # Check if file exists and get its size
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    
    file_size = file_path.stat().st_size
    print(f"Searching for '{args.phrase}' in {args.file}")
    print(f"File size: {format_file_size(file_size)}")
    print(f"Case sensitive: {not args.ignore_case}")
    print("-" * 60)
    
    match_count = 0
    
    try:
        if args.use_mmap:
            # Use memory-mapped file method
            print("Using memory-mapped file for search...")
            for byte_pos, line_num in search_phrase_mmap(
                args.file, args.phrase, not args.ignore_case
            ):
                match_count += 1
                
                if not args.count_only:
                    print(f"Match {match_count}: Line {line_num}, Byte position {byte_pos}")
                
                if args.max_results and match_count >= args.max_results:
                    print(f"\nReached maximum results limit ({args.max_results})")
                    break
        else:
            # Use streaming method
            print("Using streaming search...")
            for line_num, pos, line_content in search_phrase_in_file(
                args.file, args.phrase, not args.ignore_case
            ):
                match_count += 1
                
                if not args.count_only:
                    print(f"Match {match_count}: Line {line_num}, Position {pos}")
                    print(f"  Content: {line_content}")
                    print()
                
                if args.max_results and match_count >= args.max_results:
                    print(f"\nReached maximum results limit ({args.max_results})")
                    break
                    
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.")
    
    print("-" * 60)
    print(f"Total matches found: {match_count}")

if __name__ == "__main__":
    main()