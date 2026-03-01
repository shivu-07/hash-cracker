# Hash Cracker

A powerful hash cracking tool supporting dictionary attacks and brute force methods for MD5, SHA1, SHA256, and SHA512 hashes. Built in Python for penetration testing and password security analysis.

## Features

- **Multiple Hash Algorithms**: MD5, SHA1, SHA256, SHA512
- **Dictionary Attack**: Fast wordlist-based cracking
- **Brute Force Attack**: Exhaustive search with customizable character sets
- **Batch Processing**: Crack multiple hashes from a file
- **Auto-Detection**: Automatically identifies hash type by length
- **Progress Tracking**: Real-time speed and attempt counters
- **Result Logging**: Saves cracked passwords with timestamps
- **Performance Optimized**: 300K+ hashes/second on modern hardware

## Technical Details

**Technologies Used:**
- Python 3
- hashlib for cryptographic hashing
- itertools for brute force combinations
- Multi-threaded capable architecture

**Attack Methods:**
1. **Dictionary Attack**: Compares target hash against hashed wordlist entries
2. **Brute Force Attack**: Generates all possible combinations within specified parameters
3. **Batch Mode**: Processes multiple hashes efficiently

## Installation
```bash
# Clone the repository
git clone https://github.com/shivu-07/hash-cracker.git
cd hash-cracker

# No dependencies required - uses Python standard library only
```

## Usage

### Dictionary Attack

**Basic usage:**
```bash
python3 hash_cracker.py -t 5f4dcc3b5aa765d61d8327deb882cf99 -w wordlist.txt
```

**With specific algorithm:**
```bash
python3 hash_cracker.py -t <hash> -w wordlist.txt -a sha256
```

**Save results to custom file:**
```bash
python3 hash_cracker.py -t <hash> -w wordlist.txt -o results.txt
```

### Brute Force Attack

**Lowercase letters (1-4 characters):**
```bash
python3 hash_cracker.py -t <hash> --brute --max-length 4
```

**Digits only (faster):**
```bash
python3 hash_cracker.py -t <hash> --brute --charset digits --max-length 3
```

**Alphanumeric (slower but comprehensive):**
```bash
python3 hash_cracker.py -t <hash> --brute --charset alphanumeric --max-length 3
```

**Custom length range:**
```bash
python3 hash_cracker.py -t <hash> --brute --min-length 2 --max-length 5
```

### Batch Processing

**Create a hash file (one per line):**
```bash
cat > hashes.txt << EOF
5f4dcc3b5aa765d61d8327deb882cf99
482c811da5d5b4bc6d497ffa98491e38:md5
b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3:sha1
EOF
```

**Crack all hashes:**
```bash
python3 hash_cracker.py --batch hashes.txt -w wordlist.txt
```

**Batch brute force:**
```bash
python3 hash_cracker.py --batch hashes.txt --brute --max-length 3
```

### Test Mode

**Run built-in tests:**
```bash
python3 hash_cracker.py --test
```

### Get Help
```bash
python3 hash_cracker.py -h
```

## Example Output
```
======================================================================
[*] Starting Dictionary Attack
======================================================================
[*] Target Hash: 5f4dcc3b5aa765d61d8327deb882cf99
[*] Algorithm: MD5
[*] Wordlist: test_wordlist.txt
[*] Started: 2026-03-01 17:58:28
----------------------------------------------------------------------

======================================================================
[+] PASSWORD CRACKED!
======================================================================
[+] Plain Text: password
[+] Hash: 5f4dcc3b5aa765d61d8327deb882cf99
[+] Algorithm: MD5
[+] Attempts: 2
[+] Time Elapsed: 0.00 seconds
[+] Hashing Speed: 482,992 hashes/second
======================================================================
```

## Supported Character Sets

- `lowercase` - a-z (26 characters)
- `uppercase` - A-Z (26 characters)
- `digits` - 0-9 (10 characters)
- `letters` - a-zA-Z (52 characters)
- `alphanumeric` - a-zA-Z0-9 (62 characters)
- `all` - All printable ASCII characters (94 characters)

## Performance Benchmarks

*Results on modern CPU (your mileage may vary)*

| Attack Type | Speed | Time to crack 4-char lowercase |
|-------------|-------|-------------------------------|
| Dictionary  | 300K-500K h/s | Depends on wordlist size |
| Brute Force (lowercase) | 350K-500K h/s | ~7.5 seconds |
| Brute Force (digits) | 400K-600K h/s | ~0.17 seconds |

## Wordlists

Popular wordlists for dictionary attacks:
- **rockyou.txt** - 14M passwords from real breaches
- **SecLists** - Curated security testing lists
- **CrackStation** - 1.5B password dictionary

Download rockyou.txt:
```bash
# On Kali Linux
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Or download manually
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

## Legal Disclaimer

⚠️ **IMPORTANT**: This tool is for educational purposes and authorized security testing only.

- Only crack hashes you own or have explicit permission to test
- Unauthorized password cracking may be illegal in your jurisdiction
- The author is not responsible for misuse of this tool

**Authorized Use Cases:**
- Penetration testing with written authorization
- Security research in controlled environments
- CTF competitions and security training
- Password strength auditing for your own systems

## Future Enhancements

- [ ] Rainbow table support
- [ ] GPU acceleration with hashcat integration
- [ ] Hybrid attacks (dictionary + brute force)
- [ ] Rule-based mutations (leet speak, capitalization)
- [ ] Multi-threaded performance optimization
- [ ] Integration with Have I Been Pwned API
- [ ] GUI interface

## Learning Outcomes

Building this project taught me:
- Cryptographic hash functions and their properties
- Password cracking methodologies (dictionary vs brute force)
- Algorithm optimization and performance tuning
- Command-line tool development in Python
- Security best practices for password storage
- Ethical hacking principles

## Author

**Shivalingayya Yadrami**
- GitHub: [@shivu-07](https://github.com/shivu-07)
- LinkedIn: [shivalingayya-yadrami](https://www.linkedin.com/in/shivalingayya-yadrami-297267297)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by hashcat, John the Ripper, and other professional security tools
- Built as part of cybersecurity portfolio development
- Thanks to the InfoSec community for knowledge sharing
