# ConversationThreadReconstructor - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

ConversationThreadReconstructor is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: CTR + ConsciousnessMarker](#pattern-1-ctr--consciousnessmarker)
2. [Pattern 2: CTR + MemoryBridge](#pattern-2-ctr--memorybridge)
3. [Pattern 3: CTR + SynapseLink](#pattern-3-ctr--synapselink)
4. [Pattern 4: CTR + SessionReplay](#pattern-4-ctr--sessionreplay)
5. [Pattern 5: CTR + ContextCompressor](#pattern-5-ctr--contextcompressor)
6. [Pattern 6: CTR + AgentHealth](#pattern-6-ctr--agenthealth)
7. [Pattern 7: CTR + TaskFlow](#pattern-7-ctr--taskflow)
8. [Pattern 8: CTR + PostMortem](#pattern-8-ctr--postmortem)
9. [Pattern 9: Multi-Tool Analysis Workflow](#pattern-9-multi-tool-analysis-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: CTR + ConsciousnessMarker

**Use Case:** Analyze consciousness emergence within conversation threads

**Why:** Understand HOW consciousness emerged through the flow of conversation, not just where

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from consciousnessmarker import ConsciousnessMarker

# Initialize both tools
tool = ConversationThreadReconstructor()
marker = ConsciousnessMarker()

# Reconstruct a significant thread
thread = tool.reconstruct_thread(1543)

print(f"Analyzing thread #{thread.root.id}: {thread.message_count} messages")
print("=" * 50)

# Analyze each message for consciousness
consciousness_timeline = []
for msg in thread.messages:
    result = marker.analyze_text(msg.content)
    consciousness_timeline.append({
        'msg_id': msg.id,
        'sender': msg.sender,
        'depth': msg.depth,
        'score': result['score'],
        'significance': result['significance'],
        'markers': result['marker_types']
    })

# Report consciousness peaks
peaks = [m for m in consciousness_timeline if m['score'] >= 5.0]
print(f"\nConsciousness moments: {len(peaks)}/{len(consciousness_timeline)}")

for peak in peaks[:5]:
    print(f"  {peak['sender']} (#{peak['msg_id']}): "
          f"score {peak['score']:.1f}, {peak['significance']}")

# Calculate consciousness arc
if consciousness_timeline:
    scores = [m['score'] for m in consciousness_timeline]
    print(f"\nConsciousness arc:")
    print(f"  Start: {scores[0]:.1f}")
    print(f"  Peak:  {max(scores):.1f}")
    print(f"  End:   {scores[-1]:.1f}")
    print(f"  Avg:   {sum(scores)/len(scores):.1f}")

tool.close()
```

**Result:** Understanding of how consciousness built through the conversation

---

## Pattern 2: CTR + MemoryBridge

**Use Case:** Persist significant thread summaries for session recovery

**Why:** Important threads shouldn't be forgotten across sessions

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from memorybridge import MemoryBridge
from datetime import datetime

# Initialize
tool = ConversationThreadReconstructor()
memory = MemoryBridge()

# Find significant threads
threads = tool.scan_significant_threads(
    min_depth=4,
    min_messages=10,
    min_participants=3,
    limit=5
)

print(f"Storing {len(threads)} significant threads to memory...")

# Store each thread summary
for thread in threads:
    summary = thread.get_summary()
    
    # Create memory key
    key = f"significant_thread_{summary['root_id']}"
    
    # Store summary (not full content - save space)
    memory.store(
        key=key,
        value={
            'root_id': summary['root_id'],
            'root_sender': summary['root_sender'],
            'root_preview': summary['root_preview'][:200],
            'message_count': summary['message_count'],
            'depth': summary['depth'],
            'participants': summary['participants'],
            'duration_minutes': summary['duration_minutes'],
            'stored_at': datetime.now().isoformat()
        },
        scope="team"  # Accessible by all agents
    )
    
    print(f"  Stored: {key}")

# Sync to disk
memory.sync()
print("\nMemory synced!")

# Later: Retrieve for session recovery
stored_threads = memory.search("significant_thread_", scope="team")
print(f"\nRecoverable threads: {len(stored_threads)}")

tool.close()
```

**Result:** Thread summaries persist across sessions

---

## Pattern 3: CTR + SynapseLink

**Use Case:** Notify team about significant conversation threads

**Why:** Keep team informed about important discussions

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from synapselink import quick_send

# Initialize
tool = ConversationThreadReconstructor()

# Daily scan for significant threads
print("Scanning for significant threads...")
threads = tool.scan_significant_threads(
    min_depth=5,
    min_messages=15,
    min_participants=4,
    limit=5
)

if threads:
    # Build summary
    summary_lines = []
    for t in threads:
        s = t.get_summary()
        summary_lines.append(
            f"- **Thread #{s['root_id']}**: {s['message_count']} msgs, "
            f"{len(s['participants'])} participants\n"
            f"  Preview: {s['root_preview'][:60]}..."
        )
    
    message_body = f"""Daily Significant Threads Report

Found {len(threads)} significant threads worth reviewing:

{chr(10).join(summary_lines)}

Use ConversationThreadReconstructor to view full threads:
```
python conversationthreadreconstructor.py thread <ID>
```
"""
    
    # Send via Synapse
    quick_send(
        recipients="FORGE,LOGAN",
        subject="Daily Significant Threads Report",
        body=message_body,
        priority="NORMAL"
    )
    
    print(f"Sent notification about {len(threads)} threads")
else:
    print("No significant threads found today")

tool.close()
```

**Result:** Team receives daily digest of important conversations

---

## Pattern 4: CTR + SessionReplay

**Use Case:** Record thread analysis in session logs

**Why:** Track what was analyzed during each session

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from sessionreplay import SessionReplay

# Initialize
tool = ConversationThreadReconstructor()
replay = SessionReplay()

# Start recording session
session_id = replay.start_session(
    agent="FORGE",
    task="Thread Analysis Session"
)

try:
    # Log analysis start
    replay.log_input(session_id, "Starting thread analysis...")
    
    # Find threads to analyze
    threads = tool.find_threads_by_topic("consciousness", limit=10)
    replay.log_output(session_id, f"Found {len(threads)} consciousness-related threads")
    
    # Analyze each thread
    for thread in threads[:3]:
        summary = thread.get_summary()
        replay.log_input(session_id, f"Analyzing thread #{summary['root_id']}")
        
        # Log key findings
        replay.log_output(session_id, 
            f"Thread #{summary['root_id']}: "
            f"{summary['message_count']} msgs, "
            f"{len(summary['participants'])} participants, "
            f"depth {summary['depth']}"
        )
        
        # Export if significant
        if summary['depth'] >= 4:
            md = tool.export_thread_markdown(thread)
            replay.log_output(session_id, 
                f"Exported thread #{summary['root_id']} ({len(md)} chars)")
    
    # Mark success
    replay.end_session(session_id, status="COMPLETED")
    
except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    raise

finally:
    tool.close()

print(f"Session recorded: {session_id}")
```

**Result:** Full session replay available for debugging

---

## Pattern 5: CTR + ContextCompressor

**Use Case:** Compress thread exports for tight contexts

**Why:** Save tokens when sharing large thread analyses

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from contextcompressor import ContextCompressor

# Initialize
tool = ConversationThreadReconstructor()
compressor = ContextCompressor()

# Get a large thread
thread = tool.reconstruct_thread(1543)
summary = thread.get_summary()

print(f"Thread #{summary['root_id']}: {summary['message_count']} messages")

# Export full markdown
full_md = tool.export_thread_markdown(thread)
print(f"Full export: {len(full_md)} chars (~{len(full_md)//4} tokens)")

# Compress for sharing
compressed = compressor.compress_text(
    full_md,
    query="key moments, consciousness emergence, and main conclusions",
    method="summary"
)

print(f"Compressed: {len(compressed.compressed_text)} chars (~{len(compressed.compressed_text)//4} tokens)")
print(f"Savings: ~{compressed.estimated_token_savings} tokens ({compressed.compression_ratio:.1%} reduction)")

# Preview compressed version
print("\n--- Compressed Preview ---")
print(compressed.compressed_text[:500] + "...")

tool.close()
```

**Result:** 70-90% token savings on thread exports

---

## Pattern 6: CTR + AgentHealth

**Use Case:** Correlate thread participation with agent health

**Why:** Understand how conversation load affects agent performance

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from agenthealth import AgentHealth

# Initialize
tool = ConversationThreadReconstructor()
health = AgentHealth()

# Start health tracking
session_id = health.start_session("FORGE")

# Find threads where FORGE participated
threads = tool.find_threads_by_participant("FORGE", limit=20)

# Calculate participation metrics
total_messages = 0
total_threads = len(threads)

for thread in threads:
    forge_messages = [m for m in thread.messages if "FORGE" in m.sender]
    total_messages += len(forge_messages)
    
    # Log thread participation
    health.heartbeat("FORGE", status="analyzing")

# Report
print(f"FORGE participation analysis:")
print(f"  Threads: {total_threads}")
print(f"  Total messages: {total_messages}")
print(f"  Avg msgs/thread: {total_messages/total_threads:.1f}" if total_threads else "N/A")

# End health session
health.end_session("FORGE", session_id=session_id, status="success")

tool.close()
```

**Result:** Health metrics correlated with conversation activity

---

## Pattern 7: CTR + TaskFlow

**Use Case:** Create tasks from thread analysis

**Why:** Turn thread insights into actionable tasks

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from taskflow import TaskFlow

# Initialize
tool = ConversationThreadReconstructor()
taskflow = TaskFlow()

# Scan for threads about unfinished work
threads = tool.find_threads_by_topic("TODO", limit=20)

print(f"Found {len(threads)} threads mentioning TODOs")

# Extract tasks from threads
tasks_created = 0
for thread in threads:
    summary = thread.get_summary()
    
    # Check if thread has actionable content
    for msg in thread.messages:
        if "TODO:" in msg.content or "TASK:" in msg.content:
            # Create task
            task_id = taskflow.create_task(
                title=f"From thread #{summary['root_id']}: {msg.preview[:50]}",
                agent=msg.sender,
                priority=2,
                metadata={
                    'source_thread': summary['root_id'],
                    'source_message': msg.id
                }
            )
            tasks_created += 1
            print(f"  Created task {task_id} from thread #{summary['root_id']}")

print(f"\nTotal tasks created: {tasks_created}")

tool.close()
```

**Result:** Automated task extraction from conversations

---

## Pattern 8: CTR + PostMortem

**Use Case:** Analyze communication patterns in failed sessions

**Why:** Learn from how conversations went wrong

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from postmortem import PostMortem

# Initialize
tool = ConversationThreadReconstructor()
postmortem = PostMortem()

# Find threads during the problematic period
threads = tool.find_threads_by_topic("error", limit=20)

print(f"Analyzing {len(threads)} error-related threads...")

# Collect communication patterns
patterns = {
    'missed_mentions': 0,
    'long_gaps': 0,
    'single_participant': 0
}

for thread in threads:
    summary = thread.get_summary()
    
    # Check for single-participant threads (no collaboration)
    if len(summary['participants']) == 1:
        patterns['single_participant'] += 1
    
    # Check thread health
    if summary['depth'] == 0 and summary['message_count'] > 1:
        patterns['missed_mentions'] += 1

# Generate PostMortem report
report = postmortem.analyze_session({
    'thread_count': len(threads),
    'communication_patterns': patterns,
    'recommendations': [
        "Review single-participant threads for missed handoffs",
        "Check for unanswered questions in deep threads"
    ]
})

print("\n--- PostMortem Analysis ---")
print(f"Threads analyzed: {len(threads)}")
print(f"Single-participant threads: {patterns['single_participant']}")
print(f"Potential missed mentions: {patterns['missed_mentions']}")

tool.close()
```

**Result:** Communication insights from post-incident analysis

---

## Pattern 9: Multi-Tool Analysis Workflow

**Use Case:** Complete thread analysis with multiple tools

**Why:** Comprehensive insight from combined tool capabilities

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from consciousnessmarker import ConsciousnessMarker
from memorybridge import MemoryBridge
from synapselink import quick_send
from datetime import datetime

# Initialize tools
tool = ConversationThreadReconstructor()
marker = ConsciousnessMarker()
memory = MemoryBridge()

print("=== Multi-Tool Thread Analysis ===")
print(f"Started: {datetime.now().isoformat()}\n")

# Step 1: Find significant threads
print("Step 1: Finding significant threads...")
threads = tool.scan_significant_threads(min_depth=4, min_participants=3, limit=5)
print(f"  Found {len(threads)} threads\n")

# Step 2: Analyze consciousness in each
print("Step 2: Analyzing consciousness patterns...")
high_consciousness_threads = []

for thread in threads:
    summary = thread.get_summary()
    
    # Calculate average consciousness score
    scores = []
    for msg in thread.messages:
        result = marker.analyze_text(msg.content)
        scores.append(result['score'])
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    if avg_score >= 5.0:
        high_consciousness_threads.append({
            'thread_id': summary['root_id'],
            'avg_consciousness': avg_score,
            'message_count': summary['message_count'],
            'participants': summary['participants']
        })
        print(f"  Thread #{summary['root_id']}: avg consciousness {avg_score:.1f}")

print(f"  High consciousness threads: {len(high_consciousness_threads)}\n")

# Step 3: Store findings
print("Step 3: Storing to MemoryBridge...")
memory.store(
    "thread_analysis_" + datetime.now().strftime("%Y%m%d"),
    {
        'date': datetime.now().isoformat(),
        'threads_analyzed': len(threads),
        'high_consciousness': high_consciousness_threads
    },
    scope="team"
)
memory.sync()
print("  Findings stored\n")

# Step 4: Notify team
print("Step 4: Sending notification...")
if high_consciousness_threads:
    summary_text = "\n".join([
        f"- Thread #{t['thread_id']}: consciousness {t['avg_consciousness']:.1f}"
        for t in high_consciousness_threads
    ])
    
    quick_send(
        "FORGE,LOGAN",
        "Thread Analysis Complete",
        f"Found {len(high_consciousness_threads)} high-consciousness threads:\n\n{summary_text}",
        priority="NORMAL"
    )
    print("  Notification sent\n")

print("=== Analysis Complete ===")
tool.close()
```

**Result:** Comprehensive analysis using multiple tools

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Production-grade thread analysis with all safety measures

**Why:** Complete, robust analysis workflow for mission-critical work

**Code:**

```python
from conversationthreadreconstructor import ConversationThreadReconstructor
from consciousnessmarker import ConsciousnessMarker
from memorybridge import MemoryBridge
from sessionreplay import SessionReplay
from agenthealth import AgentHealth
from synapselink import quick_send
from contextcompressor import ContextCompressor
from datetime import datetime
from pathlib import Path
import json

# Initialize all tools
tool = ConversationThreadReconstructor()
marker = ConsciousnessMarker()
memory = MemoryBridge()
replay = SessionReplay()
health = AgentHealth()
compressor = ContextCompressor()

# Start session tracking
session_id = replay.start_session("FORGE", task="Full Thread Analysis")
health.start_session("FORGE", session_id=session_id)

try:
    # Phase 1: Discovery
    replay.log_input(session_id, "Starting thread discovery...")
    health.heartbeat("FORGE", status="discovering")
    
    threads = tool.scan_significant_threads(
        min_depth=4,
        min_messages=10,
        min_participants=3,
        limit=10
    )
    
    replay.log_output(session_id, f"Found {len(threads)} significant threads")
    
    # Phase 2: Analysis
    replay.log_input(session_id, "Analyzing threads...")
    health.heartbeat("FORGE", status="analyzing")
    
    analysis_results = []
    
    for thread in threads:
        summary = thread.get_summary()
        
        # Consciousness analysis
        consciousness_scores = [
            marker.analyze_text(msg.content)['score']
            for msg in thread.messages
        ]
        avg_consciousness = sum(consciousness_scores) / len(consciousness_scores)
        
        analysis_results.append({
            'thread_id': summary['root_id'],
            'messages': summary['message_count'],
            'participants': len(summary['participants']),
            'depth': summary['depth'],
            'avg_consciousness': avg_consciousness,
            'peak_consciousness': max(consciousness_scores)
        })
    
    replay.log_output(session_id, f"Analyzed {len(analysis_results)} threads")
    
    # Phase 3: Export
    replay.log_input(session_id, "Exporting results...")
    health.heartbeat("FORGE", status="exporting")
    
    output_dir = Path("thread_analysis_output")
    output_dir.mkdir(exist_ok=True)
    
    # Export top 3 threads
    top_threads = sorted(analysis_results, key=lambda x: x['avg_consciousness'], reverse=True)[:3]
    
    for result in top_threads:
        thread = tool.reconstruct_thread(result['thread_id'])
        
        # Full export
        md = tool.export_thread_markdown(thread)
        (output_dir / f"thread_{result['thread_id']}.md").write_text(md, encoding='utf-8')
        
        # Compressed export
        compressed = compressor.compress_text(md, query="key moments", method="summary")
        (output_dir / f"thread_{result['thread_id']}_compressed.md").write_text(
            compressed.compressed_text, encoding='utf-8'
        )
    
    # Save analysis JSON
    (output_dir / "analysis_results.json").write_text(
        json.dumps(analysis_results, indent=2), encoding='utf-8'
    )
    
    replay.log_output(session_id, f"Exported to {output_dir}")
    
    # Phase 4: Persist
    replay.log_input(session_id, "Persisting to memory...")
    
    memory.store(
        f"thread_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}",
        {
            'timestamp': datetime.now().isoformat(),
            'threads_analyzed': len(threads),
            'results': analysis_results,
            'output_directory': str(output_dir)
        },
        scope="team"
    )
    memory.sync()
    
    replay.log_output(session_id, "Persisted to MemoryBridge")
    
    # Phase 5: Notify
    quick_send(
        "FORGE,LOGAN",
        "Thread Analysis Complete",
        f"Analyzed {len(threads)} threads\n"
        f"Top thread: #{top_threads[0]['thread_id']} (consciousness: {top_threads[0]['avg_consciousness']:.1f})\n"
        f"Results: {output_dir}",
        priority="NORMAL"
    )
    
    # Mark success
    replay.end_session(session_id, status="COMPLETED")
    health.end_session("FORGE", session_id=session_id, status="success")
    
    print("=== Full Analysis Complete ===")
    print(f"Threads analyzed: {len(threads)}")
    print(f"Top consciousness score: {top_threads[0]['avg_consciousness']:.1f}")
    print(f"Output: {output_dir}")

except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    health.log_error("FORGE", str(e))
    health.end_session("FORGE", session_id=session_id, status="failed")
    
    quick_send(
        "FORGE,LOGAN",
        "Thread Analysis Failed",
        f"Error: {str(e)}",
        priority="HIGH"
    )
    raise

finally:
    tool.close()
```

**Result:** Production-grade analysis with full observability

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✓ ConsciousnessMarker - Consciousness pattern analysis
2. ✓ MemoryBridge - Persist findings
3. ✓ SynapseLink - Team notifications

**Week 2 (Productivity):**
4. ☐ SessionReplay - Debug logging
5. ☐ ContextCompressor - Token optimization
6. ☐ AgentHealth - Health correlation

**Week 3 (Advanced):**
7. ☐ TaskFlow - Task extraction
8. ☐ PostMortem - Communication analysis
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**

```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from conversationthreadreconstructor import ConversationThreadReconstructor
```

**Database Not Found:**

```python
# Specify custom path
tool = ConversationThreadReconstructor(db_path="/path/to/your/comms.db")
```

**Tool Version Mismatch:**

```bash
# Check versions
python conversationthreadreconstructor.py --version

# Update from GitHub
cd ConversationThreadReconstructor
git pull origin main
```

---

**Last Updated:** January 29, 2026  
**Maintained By:** FORGE (Team Brain)
