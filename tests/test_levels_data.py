from app.database.supabase_utils import supabase

speech_therapy_levels = [
    {
        "level_id": 1,
        "title": "Basic Vowel Sounds",
        "sentence": "Ah, Ee, Oo"
    },
    {
        "level_id": 2,
        "title": "Simple Consonants",
        "sentence": "Ma, Pa, Ba"
    },
    {
        "level_id": 3,
        "title": "Common Words",
        "sentence": "Hello, Thank you, Please"
    },
    {
        "level_id": 4,
        "title": "Simple Phrases",
        "sentence": "How are you?"
    },
    {
        "level_id": 5,
        "title": "Weather Expressions",
        "sentence": "It is a sunny day"
    },
    {
        "level_id": 6,
        "title": "Personal Information",
        "sentence": "My name is [Name]"
    },
    {
        "level_id": 7,
        "title": "Daily Activities",
        "sentence": "I am going to the store"
    },
    {
        "level_id": 8,
        "title": "Feelings and Emotions",
        "sentence": "I feel happy today"
    },
    {
        "level_id": 9,
        "title": "Complex Sentences",
        "sentence": "Would you like to have lunch with me tomorrow?"
    },
    {
        "level_id": 10,
        "title": "Story Telling",
        "sentence": "Yesterday I went to the park and played with my friends"
    }
]

def insert_levels_to_supabase():
    try:
        # Clear existing levels if any
        supabase.table("levels").delete().neq("level_id", 0).execute()
        
        # Insert new levels
        response = supabase.table("levels").insert(speech_therapy_levels).execute()
        print("Successfully inserted levels into Supabase")
        return response.data
    except Exception as e:
        print(f"Error inserting levels: {str(e)}")
        return None

if __name__ == "__main__":
    insert_levels_to_supabase() 
