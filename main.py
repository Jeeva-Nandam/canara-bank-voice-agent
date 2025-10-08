from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elevenlabs import ElevenLabs
import os, uvicorn
from dotenv import load_dotenv


load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
AGENT_PHONE_NUMBER_ID = os.getenv("AGENT_PHONE_NUMBER_ID")


client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

app = FastAPI(title="ElevenLabs Twilio Outbound Call API")


class CallRequest(BaseModel):
    to_number: str

@app.post("/make_call")
async def make_call(request: CallRequest):
    """

    :param request: Phone number of a person to be called
    :return: Request tab
    """
    try:
        response = client.conversational_ai.twilio.outbound_call(
            agent_id=AGENT_ID,
            agent_phone_number_id=AGENT_PHONE_NUMBER_ID,
            to_number=request.to_number
        )
        return {
            "status": "success",
            "conversation_id": response.conversation_id,
            "callSid": response.call_sid
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")