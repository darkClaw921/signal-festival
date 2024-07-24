from chat import GPT
from pprint import pprint   
gpt=GPT()

url='https://strana.com/tmn/'
# promt=gpt.load_prompt(url)
promt='сколько стоит дом в тюмени? вот на этом сайте https://strana.com/tmn/'
historyList = [ 
    {"role": "user", "content": 'Привет'},
    # {"role": "system", "content": 'Привет, как дела?'}
    ]

a = gpt.answer(system=promt, topic=historyList)
pprint(a)