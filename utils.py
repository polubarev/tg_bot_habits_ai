habits_tools = [
    {
        "type": "function",
        "function": {
            "name": "habit_and_diary_extraction",
            "description": "Extracts specific habit tracking and diary details from a transcription of daily activities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sleep": {
                        "type": "integer",
                        "description": "Number of hours the person slept."
                    },
                    "morning_exercises": {
                        "type": "boolean",
                        "description": "Whether the person did morning exercises or not."
                    },
                    "training": {
                        "type": "boolean",
                        "description": "Whether the person did any training or workout during the day."
                    },
                    "alcohol": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 3,
                        "description": "Alcohol consumption level from 1 to 5."
                    },
                    "mood": {
                        "type": [
                            "integer",
                            "null"
                        ],
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Mood level on a scale from 1 to 5, where 1 is very bad and 5 is very good. If the person did not explicitly mention a mood level, set this value to null."
                    },
                    "sex": {
                        "type": "boolean",
                        "description": "Whether the person had sex."
                    },
                    "masturbation": {
                        "type": "integer",
                        "description": "Whether the person had masturbation."
                    },
                    "diary": {
                        "type": "string",
                        "description": "A brief diary entry summarizing the key events and activities of the day."
                    }
                },
                "required": [
                    "sleep",
                    "morning_exercises",
                    "training",
                    "alcohol",
                    "mood",
                    "sex",
                    "masturbation",
                    "diary"
                ]
            },
            "strict": False
        }
    }
]
