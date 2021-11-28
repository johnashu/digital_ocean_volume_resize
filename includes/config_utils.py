import os
from dotenv import dotenv_values, find_dotenv


def create_data_path(pth: str, data_path: str = "logs") -> os.path:
    cwd = os.getcwd()
    p = os.path.join(cwd, data_path, pth)
    if not os.path.exists(p):
        os.mkdir(p)
    return p

class Envs:
    def __init__(self, **kw):
        self.load_envs()

    def load_envs(self):
        config = dotenv_values(find_dotenv())
        print(config)
    
        for k, v in config.items():
            try:    
                setattr(self, k, int(v))
            except (SyntaxError, ValueError):
                setattr(self, k, True if v.lower() == "true" else  False if v.lower() == "false" else v)