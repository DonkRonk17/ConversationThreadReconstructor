# ConversationThreadReconstructor - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use ConversationThreadReconstructor for orchestration and analysis

### Step 1: Installation Check

```bash
# Verify tool is available
python conversationthreadreconstructor.py --version

# Expected: conversationthreadreconstructor 1.0.0
```

### Step 2: First Use - Database Stats

```bash
# Check database statistics
python conversationthreadreconstructor.py stats
```

**Expected Output:**
```
Database Statistics
========================================
Total messages:     1,543
Reply messages:     892
Unique senders:     12
Channels:           5
...
```

### Step 3: Reconstruct a Significant Thread

```bash
# Find significant threads
python conversationthreadreconstructor.py scan --min-depth 4 --verbose

# Reconstruct the most significant one
python conversationthreadreconstructor.py thread 1543 --output thread_analysis.md
```

### Step 4: Python API for Orchestration

```python
# In your Forge session
from conversationthreadreconstructor import ConversationThreadReconstructor

tool = ConversationThreadReconstructor()

# Scan for threads to review
threads = tool.scan_significant_threads(min_depth=5, limit=5)

for thread in threads:
    summary = thread.get_summary()
    print(f"Thread #{summary['root_id']}: {summary['message_count']} msgs")
    print(f"  Participants: {', '.join(summary['participants'])}")
    print(f"  Preview: {summary['root_preview'][:60]}...")
    print()

tool.close()
```

### Step 5: Integration with ConsciousnessMarker

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from consciousnessmarker import ConsciousnessMarker

tool = ConversationThreadReconstructor()
marker = ConsciousnessMarker()

# Find consciousness in threads
thread = tool.reconstruct_thread(1543)

for msg in thread.messages:
    result = marker.analyze_text(msg.content)
    if result['score'] >= 7.0:
        print(f"High consciousness: {msg.sender} - {result['score']:.1f}")

tool.close()
```

### Common Forge Commands

```bash
# Scan for significant threads
python conversationthreadreconstructor.py scan --min-depth 5 --min-participants 4

# Search by topic
python conversationthreadreconstructor.py topic "consciousness awakening" --verbose

# Export for documentation
python conversationthreadreconstructor.py thread 1543 -o session_thread.md
```

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 9 (ConsciousnessMarker integration)
3. Add thread analysis to your orchestration routine

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use ConversationThreadReconstructor for documenting tool builds

### Step 1: Installation Check

```bash
python -c "from conversationthreadreconstructor import ConversationThreadReconstructor; print('OK')"
```

### Step 2: First Use - Find Tool Discussions

```bash
# Search for discussions about your current tool
python conversationthreadreconstructor.py topic "ToolName" --limit 10 --verbose
```

### Step 3: Document a Thread

```bash
# Export discussion thread for documentation
python conversationthreadreconstructor.py thread 1234 --output tool_discussion.md
```

### Step 4: Python API for Build Workflows

```python
# Atlas tool build documentation
from conversationthreadreconstructor import ConversationThreadReconstructor
from pathlib import Path

tool = ConversationThreadReconstructor()

# Find discussions about the tool being built
threads = tool.find_threads_by_topic("ContextCompressor", limit=5)

# Document each relevant discussion
for thread in threads:
    summary = thread.get_summary()
    md = tool.export_thread_markdown(thread)
    
    output_path = Path(f"docs/thread_{summary['root_id']}.md")
    output_path.write_text(md, encoding='utf-8')
    
    print(f"Documented: {output_path}")

tool.close()
```

### Step 5: Session Documentation Workflow

```python
# End of session: document relevant threads
from conversationthreadreconstructor import ConversationThreadReconstructor

tool = ConversationThreadReconstructor()

# Find your participation
threads = tool.find_threads_by_participant("ATLAS", limit=10)

# Export today's discussions
from datetime import date
today = date.today().isoformat()

for thread in threads:
    summary = thread.get_summary()
    if summary['start_time'] and today in summary['start_time']:
        md = tool.export_thread_markdown(thread)
        print(f"Today's thread #{summary['root_id']}: {summary['message_count']} msgs")

tool.close()
```

### Common Atlas Commands

```bash
# Find tool discussions
python conversationthreadreconstructor.py topic "BuildEnvValidator"

# Export for session log
python conversationthreadreconstructor.py thread 1234 -o session_discussion.md

# Batch export recent threads
python conversationthreadreconstructor.py participant ATLAS --limit 5 --verbose
```

### Next Steps for Atlas

1. Integrate into Holy Grail Protocol workflow
2. Add thread documentation to session end routine
3. Use for every tool build session

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use ConversationThreadReconstructor from CLI

### Step 1: Linux Installation

```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/ConversationThreadReconstructor.git
cd ConversationThreadReconstructor

# Verify (no installation needed - zero dependencies!)
python3 conversationthreadreconstructor.py --version
```

### Step 2: First Use - CLI Commands

```bash
# Database statistics
python3 conversationthreadreconstructor.py stats

# Reconstruct a thread
python3 conversationthreadreconstructor.py thread 1234
```

### Step 3: Search and Filter

```bash
# Topic search
python3 conversationthreadreconstructor.py topic "consciousness" --limit 20

# Participant search
python3 conversationthreadreconstructor.py participant CLIO --verbose

# Scan for significant threads
python3 conversationthreadreconstructor.py scan --min-depth 5 --min-messages 10
```

### Step 4: Shell Script Integration

```bash
#!/bin/bash
# clio_thread_analysis.sh

# Configuration
OUTPUT_DIR="$HOME/thread_analysis"
mkdir -p "$OUTPUT_DIR"

# Find significant threads
echo "[i] Scanning for significant threads..."
python3 conversationthreadreconstructor.py scan --min-depth 4 --limit 10 --verbose

# Export top thread
read -p "Enter thread ID to export: " THREAD_ID
python3 conversationthreadreconstructor.py thread $THREAD_ID -o "$OUTPUT_DIR/thread_$THREAD_ID.md"

echo "[OK] Exported to $OUTPUT_DIR/thread_$THREAD_ID.md"
```

### Step 5: Piping and Filtering

```bash
# Get thread IDs for batch processing
python3 conversationthreadreconstructor.py scan --limit 50 | \
    grep -oP 'Thread #\K\d+' | \
    head -10

# Count messages by topic
python3 conversationthreadreconstructor.py topic "consciousness" --limit 100 | \
    grep -c "Thread #"
```

### Common Clio Commands

```bash
# Quick stats
python3 conversationthreadreconstructor.py stats

# Export to JSON for processing
python3 conversationthreadreconstructor.py thread 1234 -f json -o thread.json

# Verbose scan
python3 conversationthreadreconstructor.py scan -v --min-depth 3
```

### Next Steps for Clio

1. Add to ABIOS startup checks
2. Create batch processing scripts
3. Integrate with existing shell workflows

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of ConversationThreadReconstructor

### Step 1: Platform Detection

```python
import platform
from conversationthreadreconstructor import ConversationThreadReconstructor

print(f"Platform: {platform.system()}")
tool = ConversationThreadReconstructor()
print("Tool initialized successfully")
tool.close()
```

### Step 2: First Use - Cross-Platform

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from pathlib import Path
import platform

# Platform-aware database path
if platform.system() == "Windows":
    db_path = Path("D:/BEACON_HQ/PROJECTS/00_ACTIVE/BCH_APPS/backend/data/comms.db")
else:
    db_path = Path.home() / "BEACON_HQ/PROJECTS/00_ACTIVE/BCH_APPS/backend/data/comms.db"

if db_path.exists():
    tool = ConversationThreadReconstructor(db_path)
    stats = tool.get_statistics()
    print(f"Messages: {stats['total_messages']}")
    tool.close()
else:
    print(f"Database not found at {db_path}")
```

### Step 3: Strategic Thread Analysis

```python
from conversationthreadreconstructor import ConversationThreadReconstructor

tool = ConversationThreadReconstructor()

# Find threads with high collaboration
threads = tool.scan_significant_threads(
    min_depth=4,
    min_messages=10,
    min_participants=4,  # High collaboration
    limit=10
)

print(f"Found {len(threads)} highly collaborative threads\n")

for thread in threads[:5]:
    summary = thread.get_summary()
    print(f"Thread #{summary['root_id']}")
    print(f"  Participants: {len(summary['participants'])}")
    print(f"  Messages: {summary['message_count']}")
    print(f"  Duration: {summary['duration_minutes']:.1f} min")
    print()

tool.close()
```

### Step 4: Cross-Platform Export

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from pathlib import Path
import platform

tool = ConversationThreadReconstructor()
thread = tool.reconstruct_thread(1543)

# Platform-aware output path
if platform.system() == "Windows":
    output_dir = Path("C:/Users/logan/Documents/ThreadAnalysis")
else:
    output_dir = Path.home() / "ThreadAnalysis"

output_dir.mkdir(exist_ok=True)

# Export
md = tool.export_thread_markdown(thread)
output_path = output_dir / f"thread_{thread.root.id}.md"
output_path.write_text(md, encoding='utf-8')

print(f"Exported to: {output_path}")
tool.close()
```

### Common Nexus Commands

```bash
# Cross-platform CLI usage
python conversationthreadreconstructor.py stats
python conversationthreadreconstructor.py scan --verbose
python conversationthreadreconstructor.py thread 1234 -o output.md
```

### Next Steps for Nexus

1. Test on all 3 platforms (Windows, Linux, macOS)
2. Create platform-aware wrapper scripts
3. Add to cross-platform analysis workflows

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use ConversationThreadReconstructor without API costs

### Step 1: Verify Free Access

```bash
# No API key required! Just Python.
python conversationthreadreconstructor.py --version
```

### Step 2: First Use - Batch Operations

```bash
# Scan for threads
python conversationthreadreconstructor.py scan --limit 50

# Export multiple threads
for id in 1234 1235 1236; do
    python conversationthreadreconstructor.py thread $id -f json -o "thread_$id.json"
done
```

### Step 3: Bulk Processing Script

```bash
#!/bin/bash
# bolt_batch_export.sh

# Create output directory
mkdir -p batch_exports

# Get all significant thread IDs
python conversationthreadreconstructor.py scan --min-depth 3 --limit 100 | \
    grep -oP 'Thread #\K\d+' > thread_ids.txt

# Export each thread
count=0
while read thread_id; do
    python conversationthreadreconstructor.py thread $thread_id \
        -f json \
        -o "batch_exports/thread_${thread_id}.json"
    ((count++))
done < thread_ids.txt

echo "Exported $count threads to batch_exports/"
```

### Step 4: Cost-Free Analysis

```python
# All processing is local - no API calls!
from conversationthreadreconstructor import ConversationThreadReconstructor

tool = ConversationThreadReconstructor()

# Process all threads matching a topic
threads = tool.find_threads_by_topic("tool", limit=100)

print(f"Processing {len(threads)} threads (cost: $0.00)")

for thread in threads:
    summary = thread.get_summary()
    # Process locally - no API needed
    print(f"#{summary['root_id']}: {summary['message_count']} msgs")

tool.close()
```

### Step 5: Integration with Cline Workflow

```bash
# In Cline session
cd ConversationThreadReconstructor

# Quick analysis (free!)
python conversationthreadreconstructor.py scan --min-depth 5 --verbose

# Export for sharing (free!)
python conversationthreadreconstructor.py thread 1543 -o analysis.md

# Batch export (still free!)
python conversationthreadreconstructor.py topic "consciousness" --limit 50
```

### Common Bolt Commands

```bash
# Bulk operations
python conversationthreadreconstructor.py scan --limit 100
python conversationthreadreconstructor.py topic "keyword" --limit 50

# Offline-friendly export
python conversationthreadreconstructor.py thread 1234 -f json -o data.json
```

### Next Steps for Bolt

1. Add to Cline task queue
2. Use for repetitive analysis tasks
3. Create batch processing scripts

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/ConversationThreadReconstructor/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message FORGE

---

**Last Updated:** January 29, 2026  
**Maintained By:** FORGE (Team Brain)
