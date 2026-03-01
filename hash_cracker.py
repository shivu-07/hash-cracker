import hashlib
import time
import argparse
import itertools
import string
import json
from pathlib import Path
from datetime import datetime


def hash_string(text, algorithm='md5'):
    """
    Hash a string using specified algorithm
    """
    hash_algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }

    if algorithm not in hash_algorithms:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    return hash_algorithms[algorithm](text.encode()).hexdigest()


def identify_hash_type(hash_value):
    """
    Try to identify hash type by length
    """
    hash_lengths = {
        32: 'md5',
        40: 'sha1',
        64: 'sha256',
        128: 'sha512'
    }

    length = len(hash_value)
    return hash_lengths.get(length, 'unknown')


def brute_force_attack(target_hash, algorithm='md5', min_length=1, max_length=4,
                       charset='lowercase', verbose=True):
    """
    Perform brute force attack on a hash
    """
    # Define character sets
    charsets = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'letters': string.ascii_letters,
        'alphanumeric': string.ascii_letters + string.digits,
        'all': string.ascii_letters + string.digits + string.punctuation
    }

    chars = charsets.get(charset, string.ascii_lowercase)

    if verbose:
        print(f"\n{'=' * 70}")
        print(f"[*] Starting Brute Force Attack")
        print(f"{'=' * 70}")
        print(f"[*] Target Hash: {target_hash}")
        print(f"[*] Algorithm: {algorithm.upper()}")
        print(f"[*] Character Set: {charset} ({len(chars)} characters)")
        print(f"[*] Length Range: {min_length}-{max_length}")
        print(f"[*] Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Calculate total possibilities
        total = sum(len(chars) ** length for length in range(min_length, max_length + 1))
        print(f"[*] Total Possibilities: {total:,}")
        print(f"{'-' * 70}\n")

    start_time = time.time()
    attempts = 0

    try:
        for length in range(min_length, max_length + 1):
            if verbose:
                print(f"[*] Trying length {length}...")

            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                attempts += 1

                # Hash and compare
                hashed = hash_string(password, algorithm)

                if hashed == target_hash:
                    elapsed = time.time() - start_time
                    if verbose:
                        print(f"\n{'=' * 70}")
                        print(f"[+] PASSWORD CRACKED!")
                        print(f"{'=' * 70}")
                        print(f"[+] Plain Text: {password}")
                        print(f"[+] Hash: {target_hash}")
                        print(f"[+] Algorithm: {algorithm.upper()}")
                        print(f"[+] Length: {length}")
                        print(f"[+] Attempts: {attempts:,}")
                        print(f"[+] Time Elapsed: {elapsed:.2f} seconds")
                        print(f"[+] Hashing Speed: {attempts / elapsed:,.0f} hashes/second")
                        print(f"{'=' * 70}\n")
                    return password

                # Progress indicator
                if verbose and attempts % 10000 == 0:
                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0
                    print(f"[*] Progress: {attempts:,} attempts | {speed:,.0f} h/s | {elapsed:.1f}s", end='\r')

        elapsed = time.time() - start_time
        if verbose:
            print(f"\n\n{'-' * 70}")
            print(f"[-] Password Not Found")
            print(f"[-] Tried {attempts:,} combinations in {elapsed:.2f} seconds")
            print(f"[-] Average Speed: {attempts / elapsed:,.0f} hashes/second")
            print(f"{'-' * 70}\n")
        return None

    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\n\n[!] Attack interrupted by user")
        print(f"[*] Tried {attempts:,} combinations in {elapsed:.2f} seconds")
        return None


def dictionary_attack(target_hash, wordlist_path, algorithm='md5', verbose=True):
    """
    Perform dictionary attack on a hash
    """
    if verbose:
        print(f"\n{'=' * 70}")
        print(f"[*] Starting Dictionary Attack")
        print(f"{'=' * 70}")
        print(f"[*] Target Hash: {target_hash}")
        print(f"[*] Algorithm: {algorithm.upper()}")
        print(f"[*] Wordlist: {wordlist_path}")
        print(f"[*] Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'-' * 70}\n")

    start_time = time.time()
    attempts = 0

    try:
        with open(wordlist_path, 'r', encoding='latin-1', errors='ignore') as wordlist:
            for line in wordlist:
                password = line.strip()
                if not password:
                    continue

                attempts += 1

                hashed = hash_string(password, algorithm)

                if hashed == target_hash:
                    elapsed = time.time() - start_time
                    if verbose:
                        print(f"\n{'=' * 70}")
                        print(f"[+] PASSWORD CRACKED!")
                        print(f"{'=' * 70}")
                        print(f"[+] Plain Text: {password}")
                        print(f"[+] Hash: {target_hash}")
                        print(f"[+] Algorithm: {algorithm.upper()}")
                        print(f"[+] Attempts: {attempts:,}")
                        print(f"[+] Time Elapsed: {elapsed:.2f} seconds")
                        print(f"[+] Hashing Speed: {attempts / elapsed:,.0f} hashes/second")
                        print(f"{'=' * 70}\n")
                    return password

                if verbose and attempts % 10000 == 0:
                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0
                    print(f"[*] Progress: {attempts:,} attempts | {speed:,.0f} h/s | {elapsed:.1f}s elapsed", end='\r')

        elapsed = time.time() - start_time
        if verbose:
            print(f"\n\n{'-' * 70}")
            print(f"[-] Password Not Found")
            print(f"[-] Tried {attempts:,} passwords in {elapsed:.2f} seconds")
            print(f"[-] Average Speed: {attempts / elapsed:,.0f} hashes/second")
            print(f"{'-' * 70}\n")
        return None

    except FileNotFoundError:
        print(f"\n[!] Error: Wordlist file not found: {wordlist_path}")
        return None
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\n\n[!] Attack interrupted by user")
        print(f"[*] Tried {attempts:,} passwords in {elapsed:.2f} seconds")
        return None


def create_test_wordlist(filename="test_wordlist.txt"):
    """
    Create a test wordlist with common passwords
    """
    common_passwords = [
        "123456", "password", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "iloveyou", "master", "sunshine", "ashley",
        "bailey", "passw0rd", "shadow", "123123", "654321",
        "superman", "qazwsx", "michael", "football", "password123",
        "welcome", "ninja", "mustang", "password1", "123456789"
    ]

    with open(filename, 'w') as f:
        for pwd in common_passwords:
            f.write(pwd + '\n')

    return filename


def save_cracked_hash(hash_value, password, algorithm, output_file="cracked_hashes.txt"):
    """
    Save a cracked hash to file
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, 'a') as f:
        f.write(f"{timestamp} | {algorithm.upper():8} | {hash_value} | {password}\n")
    print(f"[*] Saved to {output_file}")


def load_hashes_from_file(filename):
    """
    Load hashes from a file (one per line)
    Format: hash or hash:algorithm
    """
    hashes = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Support format: hash or hash:algorithm
                if ':' in line:
                    hash_value, algo = line.split(':', 1)
                    hashes.append((hash_value.strip(), algo.strip().lower()))
                else:
                    hash_value = line.strip()
                    algo = identify_hash_type(hash_value)
                    hashes.append((hash_value, algo))

        return hashes
    except FileNotFoundError:
        print(f"[!] Error: File not found: {filename}")
        return []


def batch_crack(hash_file, wordlist=None, use_brute=False, **kwargs):
    """
    Crack multiple hashes from a file
    """
    hashes = load_hashes_from_file(hash_file)

    if not hashes:
        print("[!] No valid hashes found in file")
        return

    print(f"\n{'=' * 70}")
    print(f"[*] BATCH CRACKING MODE")
    print(f"{'=' * 70}")
    print(f"[*] Loaded {len(hashes)} hashes from {hash_file}")
    print(f"[*] Attack Mode: {'Brute Force' if use_brute else 'Dictionary'}")
    print(f"{'=' * 70}\n")

    cracked = 0
    failed = 0
    start_time = time.time()

    for idx, (hash_value, algorithm) in enumerate(hashes, 1):
        print(f"\n[*] [{idx}/{len(hashes)}] Cracking {algorithm.upper()} hash...")
        print(f"[*] Hash: {hash_value}")

        if use_brute:
            result = brute_force_attack(
                hash_value,
                algorithm,
                kwargs.get('min_length', 1),
                kwargs.get('max_length', 4),
                kwargs.get('charset', 'lowercase'),
                verbose=False
            )
        else:
            if not wordlist:
                print("[!] Wordlist required for dictionary attack")
                failed += 1
                continue
            result = dictionary_attack(hash_value, wordlist, algorithm, verbose=False)

        if result:
            print(f"[+] CRACKED: {result}")
            cracked += 1
            save_cracked_hash(hash_value, result, algorithm)
        else:
            print(f"[-] Failed to crack")
            failed += 1

    elapsed = time.time() - start_time

    print(f"\n{'=' * 70}")
    print(f"[*] BATCH RESULTS")
    print(f"{'=' * 70}")
    print(f"[+] Cracked: {cracked}/{len(hashes)} ({cracked / len(hashes) * 100:.1f}%)")
    print(f"[-] Failed: {failed}/{len(hashes)}")
    print(f"[*] Total Time: {elapsed:.2f} seconds")
    print(f"[*] Results saved to: cracked_hashes.txt")
    print(f"{'=' * 70}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Hash Cracker - Dictionary & Brute Force Attack Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Examples:
      # Dictionary attack
      python3 hash_cracker.py -t <hash> -w wordlist.txt

      # Brute force attack
      python3 hash_cracker.py -t <hash> --brute --max-length 4

      # Batch mode - crack multiple hashes
      python3 hash_cracker.py --batch hashes.txt -w wordlist.txt

      # Batch brute force
      python3 hash_cracker.py --batch hashes.txt --brute --max-length 3

      # Save result
      python3 hash_cracker.py -t <hash> -w wordlist.txt -o results.txt

    Supported Algorithms: MD5, SHA1, SHA256, SHA512
            """
    )

    parser.add_argument('-t', '--target', help='Target hash to crack')
    parser.add_argument('-w', '--wordlist', help='Path to wordlist file')
    parser.add_argument('-a', '--algorithm',
                        choices=['md5', 'sha1', 'sha256', 'sha512'],
                        help='Hash algorithm (auto-detected if not specified)')
    parser.add_argument('--brute', action='store_true',
                        help='Use brute force attack mode')
    parser.add_argument('--min-length', type=int, default=1,
                        help='Minimum password length for brute force (default: 1)')
    parser.add_argument('--max-length', type=int, default=4,
                        help='Maximum password length for brute force (default: 4)')
    parser.add_argument('--charset',
                        choices=['lowercase', 'uppercase', 'digits', 'letters', 'alphanumeric', 'all'],
                        default='lowercase',
                        help='Character set for brute force (default: lowercase)')
    parser.add_argument('--batch', help='File containing multiple hashes to crack')
    parser.add_argument('-o', '--output', default='cracked_hashes.txt',
                        help='Output file for cracked hashes (default: cracked_hashes.txt)')
    parser.add_argument('--test', action='store_true',
                        help='Run test mode with sample hashes')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Quiet mode (minimal output)')

    args = parser.parse_args()

    # Test mode
    if args.test:
        print("\n[*] Running in TEST mode...")
        print("[*] Testing Dictionary Attack...")
        print("[*] Creating test wordlist...")
        test_wordlist = create_test_wordlist()

        test_cases = [
            ("password123", "md5", "482c811da5d5b4bc6d497ffa98491e38"),
            ("letmein", "sha1", "b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3"),
            ("qwerty", "sha256", "65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5"),
        ]

        print(f"[*] Running {len(test_cases)} dictionary test cases...\n")

        for password, algo, target_hash in test_cases:
            print(f"\n[TEST] Cracking {algo.upper()} hash of '{password}'...")
            result = dictionary_attack(target_hash, test_wordlist, algo, verbose=False)
            if result == password:
                print(f"[✓] SUCCESS: Found '{result}'")
            else:
                print(f"[✗] FAILED: Expected '{password}', got '{result}'")

        # Test brute force
        print("\n\n[*] Testing Brute Force Attack...")
        brute_test = ("abc", "md5", "900150983cd24fb0d6963f7d28e17f72")
        print(f"\n[TEST] Brute forcing MD5 hash of 'abc'...")
        result = brute_force_attack(brute_test[2], 'md5', 1, 3, 'lowercase', verbose=False)
        if result == brute_test[0]:
            print(f"[✓] SUCCESS: Found '{result}'")
        else:
            print(f"[✗] FAILED: Expected '{brute_test[0]}', got '{result}'")

        return

    # Batch mode
    if args.batch:
        batch_crack(
            args.batch,
            wordlist=args.wordlist,
            use_brute=args.brute,
            min_length=args.min_length,
            max_length=args.max_length,
            charset=args.charset
        )
        return

    # Require target hash
    if not args.target:
        parser.print_help()
        print("\n[!] Error: --target is required (or use --test)")
        return

    # Auto-detect algorithm if not specified
    if not args.algorithm:
        detected = identify_hash_type(args.target)
        if detected == 'unknown':
            print(f"[!] Could not auto-detect hash type (length: {len(args.target)})")
            print("[!] Please specify algorithm with -a/--algorithm")
            return
        args.algorithm = detected
        print(f"[*] Auto-detected algorithm: {args.algorithm.upper()}")

    # Choose attack mode
    if args.brute:
        result = brute_force_attack(
            args.target,
            args.algorithm,
            args.min_length,
            args.max_length,
            args.charset,
            verbose=not args.quiet
        )
    else:
        if not args.wordlist:
            print("[!] Error: --wordlist is required for dictionary attack")
            print("[*] Or use --brute for brute force attack")
            return

        result = dictionary_attack(
            args.target,
            args.wordlist,
            args.algorithm,
            verbose=not args.quiet
        )

    if result:
        print(f"[+] Cracked! Password: {result}")
        save_cracked_hash(args.target, result, args.algorithm, args.output)
    else:
        print(f"[-] Failed to crack hash")


if __name__ == "__main__":
    main()