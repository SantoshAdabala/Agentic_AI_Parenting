import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# relative import now that conversational_agent/ is a package
from agent import root_agent

load_dotenv()

# 1) Instantiate the session service
session_service = InMemorySessionService()

initial_state = {
    "user_name": None,
    "user_preferences": {
        "likes": ["parenting tips", "baby names", "activities", "milestones"]
    },
}

APP_NAME   = "Glowva Bot"
USER_ID    = "Santosh_adabala"
SESSION_ID = str(uuid.uuid4())

# 2) Create a new session
stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

# 3) Wire the Runner with that same service instance
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# 4) Send a test message
new_message = types.Content(
    role="user",
    parts=[types.Part(text="What foods help a 2-year-old grow strong?")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message
):
    if event.is_final_response():
        print("Agent:", event.content.parts[0].text)
