def make_story(topic: str, age: str = "4-8", language: str = "English") -> dict:
    """Offline-friendly story generator. No external API key required."""
    clean = topic.strip().rstrip(".!?") or "A brave little rabbit"
    title = f"The Little Adventure of {clean[:45]}"
    templates = [
        ("A Curious Beginning", f"One bright morning, {clean} began a wonderful adventure. The world felt full of surprises, and a new day was waiting to begin.", "sunny meadow"),
        ("A Tiny Challenge", f"Along the way, {clean} discovered a small problem. It seemed tricky at first, but taking a deep breath made everything feel possible.", "forest path"),
        ("A Helpful Friend", f"Just then, a kind new friend arrived. They listened carefully, shared an idea, and decided to solve the problem together.", "friendly forest animals"),
        ("Working Together", f"Step by step, they tried again. They used patience, kindness, and teamwork instead of giving up. Soon, they could see their plan working.", "magical garden"),
        ("A Happy Ending", f"At last, {clean} and the new friend celebrated their success. They learned that courage grows when we help one another. And that was only the beginning of another adventure!", "rainbow village"),
    ]
    scenes = [{"heading": h, "narration": n, "visual": v} for h, n, v in templates]
    return {
        "title": title,
        "topic": clean,
        "language": language,
        "age": age,
        "intro": "A gentle, positive story about courage, kindness, and teamwork.",
        "scenes": scenes,
        "note": "This starter version uses a built-in story template. Connect an LLM provider to generate fully customized scripts."
    }
