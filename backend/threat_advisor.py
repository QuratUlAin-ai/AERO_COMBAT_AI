import os
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------
# SETUP
# ---------------------------
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY is missing. Please check your .env file.")
    exit()
client = OpenAI(api_key=api_key)

# ---------------------------
# Few-Shot Examples for Better Prompting
# ---------------------------
few_shot_examples = """
Example 1:
Scenario: Enemy MiG-29s approaching fast from 030 at 80 miles, altitude 22,000 ft.
Output:
- Threat Assessment: High-speed intercept from well-armed fighters with BVR capability.
- Tactical Advice: Maintain radar lock, extend to drag them into friendly SAM umbrella. Avoid merge.
- Risk Level: High
- Suggested Maneuver or Action: Cold turn south, descend to NOE (500 ft AGL), call AWACS for intercept assist.
- Comms or Coordination Notes: Request friendly CAP support on Guard Channel 2.

Example 2:
Scenario: SA-6 battery detected east of target area, overlapping flight path.
Output:
- Threat Assessment: Medium-altitude radar-guided SAM with known engagement envelope.
- Tactical Advice: Use terrain masking to approach from the west. Launch HARMs preemptively from standoff.
- Risk Level: Medium
- Suggested Maneuver or Action: Pop-up attack profile at 10 nm, fire and egress low.
- Comms or Coordination Notes: Coordinate with SEAD package on Channel 4.
"""

# ---------------------------
# Generate Tactical Advice
# ---------------------------
def generate_advice(input_text):
    prompt = f"""
You are an AI tactical advisor for real-time air combat.
Your job is to analyze the threat scenario and advise the pilot or mission lead with tactical maneuvers.

Assume NATO doctrine, modern 4th/5th gen fighters, and realistic threat environments.

Provide advice in the following format:
- Threat Assessment:
- Tactical Advice:
- Risk Level:
- Suggested Maneuver or Action:
- Comms or Coordination Notes:

{few_shot_examples}
Scenario:
{input_text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

# ---------------------------
# RUNNER
# ---------------------------
if __name__ == "__main__":
    print("\nThreat Advisor Module")
    input_text = input("\nDescribe the threat scenario: ")

    print("\nGenerating tactical advice...\n")
    advice = generate_advice(input_text)

    print("\nTactical Advice:\n")
    print(advice)
    print("\nDone.")
