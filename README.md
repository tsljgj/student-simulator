# Student Simulator

A realistic AI student that responds differently based on knowledge mastery levels (0%, 50%, 100%).

## Quick Start

### 1. Prerequisites
- Python 3.7+
- OpenAI API key

### 2. Setup
```bash
# Clone/download the project files
cd student-tutor-simulator

# Install dependencies
pip install openai>=1.30.0 python-dotenv

# Set your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. Run
```bash
python main.py
```

## Required Files

Create these files in your project directory:

```
student-tutor-simulator/
├── main.py
├── student_simulator.py
├── kc_manager.py
├── config.py
├── .env                  # Your API key here
├── prompts/
│   ├── student_base_prompt.txt
│   ├── mastery_0_prompt.txt
│   ├── mastery_50_prompt.txt
│   └── mastery_100_prompt.txt
└── data/
    └── kc_mastery.json
```

## How to Use

### Basic Interaction
```
Teacher: What is 7 + 5?
Student: That's 12! 7 + 5 = 12.

Teacher: What is 47 - 29?
Student: I don't know how to do that kind of subtraction. Can you help me?
```

### Commands
- `/status` - Show knowledge mastery levels
- `/update` - Change mastery for a topic
- `/reset` - Clear conversation history
- `/quit` - Exit

### Example: Update Knowledge
```
Teacher: /update
1. Basic Addition (currently 100%)
2. Addition with Carrying (currently 50%)
...
Enter number: 2
Enter new mastery (0, 50, or 100): 100
✓ Updated Addition with Carrying to 100% mastery
```

## How It Works

The student responds differently based on mastery:

- **100% mastery**: Confident, correct answers
- **50% mastery**: Uncertain, "I think..." responses
- **0% mastery**: "I don't know how to..." responses

## Troubleshooting

**API Key Error**: Make sure your `.env` file contains:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**File Not Found**: Ensure all files from the artifacts are created in the correct directories.

**Module Not Found**: Run `pip install openai python-dotenv`

## Get OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create account or sign in
3. Click "Create new secret key"
4. Copy the key to your `.env` file

That's it! Start teaching your AI student!