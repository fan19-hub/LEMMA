import json
from configs import prompts_root, imgbed_root, cache_root
from utils import onlineImg_process, offlineImg_process, gpt_no_image

class LemmaComponent:
    def __init__(self, prompt, name, model='gpt4-o', using_cache=False, cache_name='', online_image=True, max_retry=5,
                 max_tokens=1000, temperature=0.1, post_process=None):
        self.name = name
        self.model = model
        self.using_cache = using_cache
        self.online_image = online_image
        self.max_retry = max_retry
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.post_process = post_process

        if cache_name != '':
            self.cache_name = cache_name
        else:
            self.cache_name = self.name + '.json'

        if type(prompt) == str:
            with open(prompts_root + prompt, 'r', encoding='utf-8') as f:
                self.prompt = f.read()
        else:
            self.prompt = prompt

        if using_cache:
            try:
                with open(cache_root + self.cache_name, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except FileNotFoundError:
                self.cache = {}

    def __call__(self, *args, **kwargs):
        print(f'Lemma Component {self.name}: Starting...')
        if 'image' in kwargs:
            image_path = kwargs['image']
            del kwargs['image']
        else:
            image_path = ''
        prompt = self.prompt.format(**kwargs)
        if self.using_cache:
            if prompt in self.cache:
                print(f'Lemma Component {self.name}: retrieve from cache')
                return self.cache[prompt]
        for i in range(self.max_retry):
            try:
                if self.model == 'gpt4v':
                    if self.online_image:
                        if 'http' not in image_path:
                            image_path = imgbed_root + image_path
                        result = onlineImg_process(prompt=prompt, url=image_path,
                                                   max_tokens=self.max_tokens, temperature=self.temperature)
                    else:
                        result = offlineImg_process(prompt=prompt, image_path=image_path,
                                                    max_tokens=self.max_tokens, temperature=self.temperature)
                elif self.model == 'gpt3.5':
                    result = gpt_no_image(prompt, model='gpt-3.5-turbo', max_tokens=self.max_tokens,
                                          temperature=self.temperature)
                elif self.model == 'gpt4':
                    result = gpt_no_image(prompt, model='gpt-4o', max_tokens=self.max_tokens,
                                          temperature=self.temperature)
                else:
                    raise ValueError(f'Unknown model {self.model}')
                if self.post_process is not None:
                    result = self.post_process(result)
                break
            except Exception as e:
                print(f'Lemma Component {self.name}: {e}, retrying...')
                continue
        else:
            print(f'Lemma Component {self.name}: Max retry exceeded')
            return None

        if self.using_cache and result is not None:
            self.cache[prompt] = result
            with open(cache_root + self.cache_name, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f)

        return result
