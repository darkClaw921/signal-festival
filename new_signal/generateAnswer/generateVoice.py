import asyncio
from elevenlabs import Voice, VoiceSettings, play, save
from elevenlabs.client import AsyncElevenLabs, ElevenLabs
from pprint import pprint

eleven = AsyncElevenLabs(
  api_key="" # Defaults to ELEVEN_API_KEY
)
async def gen_audio():
    audio = await eleven.generate(
        text="Hello! My name is Bella.",
        # voice='Bill',
        # model='eleven_monolingual_v1',
        # voice=Voice(
            # voice_id='X5B3rQ1NtO5CK1qt4KrI',
            # settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        )
    pprint(audio)
    save(audio,'test.mp3')

# play(audio)
async def print_models() -> None:
    models = await eleven.models.get_all()
    print(models)

def main():
    from elevenlabs import generate, play
    
    client=ElevenLabs(
        api_key="" # Defaults to ELEVEN_API_KEY
    )
    
    audio = client.generate(
        text='Привет! Я - комьюнити-менеджер фестиваля "Сигнал". Чем я могу помочь?',
        voice="Arnold",
        model='eleven_multilingual_v1'
    )

    play(audio)

# asyncio.run(gen_audio())
main