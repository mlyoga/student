import random

# Sample event database
EVENTS = [
    {"title": "AI & ML Conference", "category": "Artificial Intelligence"},
    {"title": "Hackathon 2025", "category": "Coding"},
    {"title": "Electric Vehicles Expo", "category": "Automobile"},
    {"title": "Research Paper Submission", "category": "Academics"},
    {"title": "Cybersecurity Challenge", "category": "Cybersecurity"},
    {"title": "Renewable Energy Summit", "category": "Energy"},
]

def recommend_events(skills):
    """
    Recommend events based on user skills.
    """
    recommended = [event for event in EVENTS if any(skill.lower() in event["category"].lower() for skill in skills)]
    
    # If no exact matches, suggest random ones
    if not recommended:
        recommended = random.sample(EVENTS, min(3, len(EVENTS)))
    
    return recommended
