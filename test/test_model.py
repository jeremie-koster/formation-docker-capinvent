from src.app.model import ModelHandler
import numpy as np

model = ModelHandler()


def test_load_img():
    img = model.load_img("./examples/green_snake.jpeg")
    assert(isinstance(img, np.ndarray))
    assert(len(img.shape)==3)

def test_postProcess():
    x = np.zeros((200, 200, 3))
    x = model._preprocess(x)
    assert(isinstance(x, np.ndarray))
