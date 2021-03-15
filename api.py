import requests

def get_chuck_norris_joke():
    fallback_joke = 'Chuck Norris onced built a 4 story condo using only a loaf of bread, shoe string, and silly putty.'
    res = requests.get('https://api.chucknorris.io/jokes/random')

    if res.ok:
        joke = res.json()['value']
        return joke
    else:
        return fallback_joke


def get_cat_fact():
    res = requests.get('https://catfact.ninja/fact')

    if res.ok:
        fact = res.json()['fact']
        return fact
    else:
        return 'I love cats'
