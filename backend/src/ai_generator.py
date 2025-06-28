import os
import json
import random

from openai import OpenAI
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator. 
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:
    {
        "title": "The question title",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 0, // Index of the correct answer (0-3)
        "explanation": "Detailed explanation of why the correct answer is right"
    }

    Make sure the options are plausible but with only one clearly correct answer.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        content = response.choices[0].message.content
        challenge_data = json.loads(content)

        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data

    except Exception as e:
        print(e)
        # Provide multiple fallback challenges and randomly select one
        fallback_challenges = [
            {
                "title": "Basic Python List Operation",
                "options": [
                    "my_list.append(5)",
                    "my_list.add(5)",
                    "my_list.push(5)",
                    "my_list.insert(5)",
                ],
                "correct_answer_id": 0,
                "explanation": "In Python, append() is the correct method to add an element to the end of a list."
            },
            {
                "title": "JavaScript Array Method",
                "options": [
                    "array.push(item)",
                    "array.add(item)",
                    "array.append(item)",
                    "array.insert(item)",
                ],
                "correct_answer_id": 0,
                "explanation": "In JavaScript, push() is the correct method to add an element to the end of an array."
            },
            {
                "title": "Python Dictionary Access",
                "options": [
                    "dict['key']",
                    "dict('key')",
                    "dict->key",
                    "dict::key",
                ],
                "correct_answer_id": 0,
                "explanation": "In Python, you access dictionary values using square bracket notation with the key."
            },
            {
                "title": "SQL SELECT Statement",
                "options": [
                    "SELECT * FROM table WHERE condition;",
                    "RETRIEVE * FROM table WHERE condition;",
                    "GET * FROM table WHERE condition;",
                    "QUERY * FROM table WHERE condition;",
                ],
                "correct_answer_id": 0,
                "explanation": "In SQL, SELECT is the correct keyword to retrieve data from a database table."
            },
            {
                "title": "HTML Heading Tag",
                "options": [
                    "<h1>Heading</h1>",
                    "<heading>Heading</heading>",
                    "<head>Heading</head>",
                    "<title>Heading</title>",
                ],
                "correct_answer_id": 0,
                "explanation": "In HTML, <h1> is the correct tag for the main heading of a document."
            }
        ]

        # Filter challenges based on difficulty if needed
        if difficulty.lower() == "easy":
            # Use all challenges for easy difficulty
            filtered_challenges = fallback_challenges
        elif difficulty.lower() == "medium":
            # Use a subset for medium difficulty
            filtered_challenges = fallback_challenges[1:4]
        else:  # hard
            # Use the last two challenges for hard difficulty
            filtered_challenges = fallback_challenges[3:5]

        # Return a random challenge from the filtered list
        return random.choice(filtered_challenges)
