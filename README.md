# AssetCrafter

> ✨ Project formerly known as **[HRTool](https://t.me/HRModster)** on Telegram

**AssetCrafter** is a powerful, modular toolkit for reverse engineering and modifying compressed game archive files such as `.pak`, `.dat`, and `.obb`. Built for speed, flexibility, and usability in Termux or desktop Linux environments, it supports complex workflows including Zstandard (zstd) decompression with or without dictionaries, XOR decryption, zlib stream carving, and repacking.

---
## 📊 Project Stats

- **Total Users:** `230+`
- **Total Requests Served:** `46,100+`

---

## 🎉 Community Announcement

🔓 **Good News!**  
By popular request from the community, this private project has now been made **publicly available** on GitHub.

> ⚠️ **Note:** The core *hasher logic* is not included, as it contains sensitive authentication and encryption code critical to the integrity of our validation system.

---

## 🚀 Key Features

* **🔍 Deep Archive Analysis**
  Scans large `.pak`, `.dat`, or `.obb` files for known compression signatures and magic numbers to extract individual game assets.

* **🔒 Zstandard Support**
  Decompress segments using Zstandard with or without custom dictionaries embedded in the archive.

* **⚡ High-Speed Processing**
  Supports multithreaded decompression for dictionary-based archives, drastically improving extraction speeds.

* **🔄 Seamless Repacking**
  Modify extracted files and repack them into `.pak` files using optimized compression that fits within original segment sizes.

* **🤍 XOR Encryption & Decryption**
  Automatically detects and decodes XOR-obfuscated game files.

* **🛠️ Zlib Stream Detection**
  Uses tools like Offzip and custom C logic to locate, extract, and decompress zlib and raw deflate streams.

* **🔧 Rebuilding Tools**
  Extracted segments can be patched and merged into a valid, working `.pak` archive with byte-level control.

* **🪡 Modular Directory Structure**
  Clearly defined folder layout for original files, extracted assets, edited versions, and repacked outputs.

* **🔢 Minimal Dependency**
  Built with Python and native binaries; no bloated packages, works in Windows WSL & Android Termux with QEMU i386 emulation.

* 🔍 **Fast Hex-Based Search Tool** – Quickly scans multiple files using hex patterns instead of strings, with `tqdm`-powered progress bars and support for copying matched results.
  
* 🧩 **Smart Archive Comparer** – Compares original and modified archives to detect file differences with precision and speed.
---

## 📂 Project Description

**AssetCrafter** was designed for developers, modders, and researchers who need to analyze or modify encrypted/compressed game resource files. Many games store their assets in large monolithic `.pak` or `.dat` files that are compressed using Zstandard, zlib, or deflate, and sometimes obfuscated with XOR. These archives often lack indexes or use non-standard formats.

AssetCrafter solves this by:

* Scanning binary files for known compression headers (e.g., `0x28B52FFD`, `0x78 9C`, etc.)
* Extracting segments into standalone `.dat` chunks
* Decompressing them using Zstandard (with dictionary if required) or zlib
* Allowing user modification
* Recompressing with best-fit compression level and reassembling the full archive

---

## 💡 Concepts & Architecture

### 1. Segment-Based Extraction

Pak files are divided into compressed segments, each starting with a magic number (`0x28B52FFD`). AssetCrafter identifies these boundaries and extracts them individually.

### 2. Zstandard Compression

Supports both:

* Standard zstd compression
* Zstd with dictionary (auto-detected using `0x37A430EC` marker)

Uses the Python `zstandard` module to decompress and recompress.

### 3. XOR Decryption

For files obfuscated with XOR, the tool attempts known XOR keys or brute-force decoding using file signature matching.

### 4. Zlib Stream Extraction (Offzip Mode)

* Searches for `0x78 9C`, `0x78 DA`, etc.
* Uses Offzip logic or custom C tools to extract valid deflate/zlib streams
* Useful when analyzing embedded compressed blobs without a file table

### 5. Repacking Workflow

* Extracted segments can be modified freely
* The tool tries compressing at zstd levels 1-22 until output fits within original segment size
* Pads with `\x00` if needed for alignment
* Replaces the segment in a copy of the original `.pak`

### 6. One-File Bundle Output

Optional feature to merge all unpacked files into a single self-contained archive for easy patch distribution.

### 7. Device-Based Validation & Subscription Control

The tool includes a robust subscription validation model built on unique device identification. Each client device generates an encrypted `device_key` that is securely sent to the server. The backend (Flask) decrypts this key using AES-256-CBC and checks it against a MySQL database. If the device is recognized and has an active subscription (based on `subscription_start` and `subscription_end`), access is granted. New devices are auto-registered with a 30-day default access period. Additionally, the server updates usage stats and assigns metadata like usernames or feature access flags. This architecture ensures that only authorized devices can use the tool, supporting flexible free/premium models and real-time analytics.

### 8. High-Speed Hex Search Engine

Implements a highly efficient binary pattern scanner that searches for hex signatures across thousands of files. This approach is faster and more reliable than traditional string-based search, especially for binary formats like `.pak`, `.dat`, or `.obb`. It supports copying all or selected matching files to a new workspace for further analysis or editing.

### 9. Intelligent Archive Comparison Utility

Provides a differential comparison mechanism between two directories (e.g., original vs. modified game files). It highlights which files have been altered, added, or removed using optimized file reading techniques. This is critical for identifying game updates, mod changes, or reverse-engineering file structures.

---

## 🏢 Directory Layout

```
Tool/
├── HRModster_EXES/
├── obb/
│   ├── Original_obb/
│   ├── repacked_obb/
│   ├── Original_pak/
│   ├── repacked_pak/
│   ├── Searched_DAT/
│   ├── Edited_Dat/
│   ├── unpacked_obb/
│   ├── Compared_DAT/
│   ├── unpack_zsdic_pak/
│   ├── unpacked_pak/
│   ├── repacked_zsdic/
│   ├── original_zsdic_pak/
│   ├── edited_dat_zsdic/
│   └── unpacked_ASS_pak/
├── gamepatch/
│   ├── Original_pak/
│   ├── unpacked_ASS_DAT/
│   ├── unpacked_RAW_DAT/
│   ├── Edited_DEASS_DAT/
│   ├── repacked_pak/
│   ├── Searched_DAT/
│   ├── Edited_DAT/
│   └── Compared_DAT/
└── mappak/
    ├── Original_pak/
    ├── unpacked_ASS_DAT/
    ├── unpacked_RAW_DAT/
    ├── Edited_DEASS_DAT/
    ├── repacked_pak/
    ├── Searched_DAT/
    ├── Edited_DAT/
    └── Compared_DAT/
```

---

## 🚧 Requirements

* Python 3.x
* pip modules:

  * `zstandard`
  * `pycryptodome`
  * `tqdm`
  * `requests`
  * `colorama`
* Termux (for mobile users)
* `qemu-user-i386` if running legacy tools

---

## 📖 Usage Instructions

### 📱 Mobile Setup (Termux)
```bash
wget https://github.com/Calamivathan/HRTOOL/releases/download/%23HRTOOL_V6_PC/hr-tool-mobile.deb && dpkg -i hr-tool-mobile.deb && bash /data/data/com.termux/files/home/Tool/HRModster_EXES/cmd.sh
```
### 💻 PC Setup (WSL/ Linux)
```bash
wget https://github.com/Calamivathan/HRTOOL/releases/download/%23HRTOOL_V6_PC/hr-tool-pc.deb && dpkg -i hr-tool-pc.deb && sudo bash /data/data/com.termux/files/home/Tool/HRModster_EXES/cmd.sh
```

🔹 **What this does:**
- Each command is placed in a fenced `bash` code block.
- GitHub will automatically show a **copy** button at the top-right corner of each block.
- Avoid placing commands inside inline backticks (\`) if you want copy-on-click to work properly.

---

## 📊 Use Cases

* Game asset modding and patching
* Mobile reverse engineering research
* Compressed archive forensics
* Data extraction from proprietary or encrypted formats

---

## 🌟 Why AssetCrafter?

* Designed for both technical and casual users
* Modular, clean folder structure
* Rebuilds valid, working archives
* Portable and lightweight
* Supports modern compression methods
* Fully scriptable for automation

---

## ✉ Contributing / Contact
### ❤️ Huge thanks to our passionate private community of **340+ members** 🙌  
### Your continuous support, testing, and feedback made this public release possible! 🚀✨

This project started as "hrtool" on Telegram. For contributions, feature requests, or collaboration:

* [Telegram Channel/Group](https://t.me/HRModster_DevGC)
* [GitHub Issues](https://github.com/Calamivathan/HRTOOL/issues)

---

## ⚖️ License

MIT License. Free to use, modify, and distribute.

> © 2025 @HRModster Team. Made with passion for reverse engineering and clean code, Jai Baba Ki.
