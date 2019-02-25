
from gensim.models.doc2vec import Doc2Vec
from settings import PROJECT_NAME, UNSUPERVISED_MODELS_DIR
from settings import unsupervised_model_suffix
import os
import sys
from itertools import islice

project_folder = None
expected_env = '%sAI' % PROJECT_NAME.upper()
try:
    project_folder = os.environ[expected_env]
except KeyError:
    sys.exit('Unable to find the env %s' % expected_env)


def load_unsupervised_model(model_file: str):
    return Doc2Vec.load(model_file)


def load_unsupervised_models(only: str = 'pvdmwav'):
    unsupervised_models_dir = os.path.join(
        project_folder, UNSUPERVISED_MODELS_DIR)

    def model_loader(file): return load_unsupervised_model(
        os.path.join(unsupervised_models_dir, file))

    def model_selector(file, _only):
        if(only):
            return file == '%s_%s' % (only, unsupervised_model_suffix)
        return file.endswith(unsupervised_model_suffix)
    models = [model_loader(file) for file in os.listdir(
        unsupervised_models_dir) if model_selector(file, only)]
    return models


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


if __name__ == '__main__':
    load_unsupervised_models()
