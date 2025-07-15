from openai import OpenAI
import os
from dotenv import load_dotenv

# ---------------------------
# 🔧 SETUP
# ---------------------------
load_dotenv()
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ---------------------------
# 💡 Few-Shot Examples for Better Prompting
# ---------------------------
few_shot_examples = """
Example 1:
Input: Destroy enemy SAM sites in northern valley before main force arrives.
Output:
Mission Name: Iron Shield
Mission Type: SEAD (Suppression of Enemy Air Defenses)
Objectives: Eliminate enemy SA-6 and SA-11 systems positioned in Grid 23B before Blue Force insertion at 0600Z.
Location: Northern valley region, 23B
Timing: 0545Z–0610Z
Weather Conditions: Overcast, light rain, winds 10 knots from NW
Friendly Forces: 2x F-16CJ (Wild Weasel)
Enemy Threats: SA-6 Gainful, SA-11 Gadfly, low probability of enemy CAP
Aircraft Loadout Recommendation: AGM-88 HARM, ECM pods, external fuel tanks
Communications & Coordination: SEAD coordination with AWACS “Overwatch” on Channel 3
Risk Assessment: Medium – strong radar coverage
Rules of Engagement: PID SAM radars before launch

Example 2:
Input: Escort transport aircraft through contested airspace with radar threats.
Output:
Mission Name: Silent Guardian
Mission Type: Escort
Objectives: Protect C-130 Hercules from radar-guided threats during transit over Zone Red
Location: Corridor Alpha, Red Zone
Timing: 0930Z–1000Z
Weather Conditions: Clear skies, 15 km visibility
Friendly Forces: 2x F-15C, 1x C-130
Enemy Threats: Mobile SAMs (SA-15, SA-8), possible enemy GCI radar activation
Aircraft Loadout Recommendation: AIM-120C, ECM pods
Communications & Coordination: C-130 on Channel 1, AWACS on Channel 4
Risk Assessment: High
Rules of Engagement: Engage only if radar lock or visual confirmation of hostile behavior

Now, generate a mission briefing for the following scenario.
"""

# ---------------------------
# 📜 Prompt Template
# ---------------------------
mission_prompter = """
You are a senior combat mission planner AI trained in NATO doctrine and modern air warfare planning. 
Take the user's unstructured input and turn it into a structured and complete mission briefing.

Your output format should be as follows:
Mission Name:
Mission Type: (e.g., SEAD, CAP, Strike, Escort, Recon)
Objectives:
Location:
Timing:
Weather Conditions:
Friendly Forces:
Enemy Threats:
Aircraft Loadout Recommendation:
Communications & Coordination:
Risk Assessment:
Rules of Engagement:

{few_shots}

Input Mission Scenario:
{input_text}
"""

# ---------------------------
# Function: Generate mission briefing
# ---------------------------
def generate_mission(input_text):
    full_prompt = mission_prompter.format(
        input_text=input_text,
        few_shots=few_shot_examples
    )
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------------------------
# RUNNER
# ---------------------------
if __name__ == "__main__":
    print("\nWelcome to Mission Planner")
    user_input = input("\nEnter mission scenario as text: ")

    print("\nGenerating mission briefing...\n")

    briefing = generate_mission(user_input)
    print("\nMission Briefing:\n")
    print(briefing)

    print("\nDone.")
