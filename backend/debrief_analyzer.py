import os
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------
# 🔧 SETUP
# ---------------------------
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY is missing. Please check your .env file.")
    exit()
openai = OpenAI(api_key=api_key)

# ---------------------------
# Few-Shot Examples for Debrief Analyzer
# ---------------------------
few_shot_examples = """
Example 1:
Input (Debrief): 
Our F-16s encountered heavy SAM activity over the valley. One aircraft took damage due to delayed chaff release. Enemy fighters scrambled 5 minutes later. Poor coordination with AWACS.

Output:
- Tactical Summary:
F-16s faced unexpected SAM fire. Delayed countermeasures led to damage. Enemy air response was rapid. Comms with AWACS were inadequate.

- Key Mistakes:
• Delayed chaff deployment.
• Poor coordination with AWACS.
• Late detection of enemy scramble.

- Lessons Learned:
• Improve timing on countermeasure deployment.
• Ensure tighter integration with AWACS.
• Use earlier warning of likely enemy CAP launches.

- Recommendations:
• Simulate SAM pop-up scenarios in training.
• Standardize chaff/flare timing.
• Assign dedicated comms officer for AWACS link.

Example 2:
Input (Debrief):
Strike package was delayed over target area. GPS jamming caused route drift. Bomb release was off-target. One aircraft experienced fuel starvation during RTB.

Output:
- Tactical Summary:
Mission delay and GPS jamming disrupted strike timing and accuracy. One aircraft nearly lost during egress due to fuel issues.

- Key Mistakes:
• Failure to account for enemy GPS denial.
• Poor time-on-target coordination.
• Inadequate fuel margin planning.

- Lessons Learned:
• Pre-plan alternate navigation strategies.
• Build margin into TOT windows.
• Review fuel consumption models for strike profiles.

- Recommendations:
• Include INS-only nav drills in training.
• Assign backup lead navigator.
• Review bingo fuel protocols across flight.
"""

# ---------------------------
# Prompt Template
# ---------------------------
debrief_prompter = """
You are a post-mission analysis AI. Your task is to analyze unstructured pilot debrief notes and summarize tactical insights.

Use the following format:
- Tactical Summary:
- Key Mistakes:
- Lessons Learned:
- Recommendations:

{few_shots}

Now analyze the following debrief:

Input (Debrief):
{input_text}
"""

# ---------------------------
# GPT-Based Debrief Analysis
# ---------------------------
def analyze_debrief(input_text):
    try:
        full_prompt = debrief_prompter.format(
            input_text=input_text,
            few_shots=few_shot_examples
        )

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT analysis failed: {e}")
        return input_text

# ---------------------------
# RUNNER
# ---------------------------
if __name__ == "__main__":
    print("\nPost-Mission Debrief Analyzer")

    input_text = input("Enter pilot debrief summary: ").strip()

    if not input_text:
        print(" No input provided.")
        exit()

    # Analyze debrief
    debrief_summary = analyze_debrief(input_text)

    # Output the result
    print("\nDebrief Analysis:\n")
    print(debrief_summary)

