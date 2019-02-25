
from gensim.models.doc2vec import Doc2Vec
from multiprocessing import cpu_count
import os
import sys

from data.patentsview.corpus import PatentsViewTaggedDocument


def train_unsupervised(
        tsv_or_tsvzip: str,
        dataset_name: str,
        required_docs_count: int,
        model_folder: str):
    documents = PatentsViewTaggedDocument(
        tsv_or_tsvzip=tsv_or_tsvzip,
        dataset_name=dataset_name,
        required_docs_count=required_docs_count)
    cores = cpu_count()
    vocab = 915715  # along with paper
    model_names = ['pvdbow', 'pvdmwconcat', 'pvdmwav']
    models = [
        # PV-DBOW
        Doc2Vec(
            dm=0,
            dbow_words=1,
            vector_size=200,
            window=5,
            min_count=5,
            max_vocab_size=vocab,
            workers=cores),
        # PV-DM w/concatenation
        Doc2Vec(
            dm=1,
            dm_concat=1,
            vector_size=200,
            window=5,
            min_count=5,
            max_vocab_size=vocab,
            workers=cores),
        # PV-DM w/average
        Doc2Vec(
            dm=1,
            dm_mean=1,
            vector_size=200,
            window=5,
            min_count=5,
            max_vocab_size=vocab,
            workers=cores),
    ]
    models[0].build_vocab(documents)
    sys.stderr.write('\n Built vocabulary for %s' % model_names[0])
    for model in models[1:]:
        model.reset_from(models[0])
        sys.stderr.write('\n done %s ' % str(model))

    for index, model in enumerate(models):
        sys.stderr.write('\n Training %s' % model_names[index])
        model.train(
            documents,
            total_examples=model.corpus_count,
            epochs=10,
            start_alpha=0.002,
            end_alpha=-0.016)
        model.save(
            os.path.join(
                model_folder,
                '%s_doc2vec.model' %
                model_names[index])
        )


if __name__ == '__main__':
    usage = '''
    sys.argv[1] - datafile - tsv file
    sys.argv[2] - dataset name
    sys.argv[3] - number of records
    sys.argv[4] - target model folder
    '''
    if(len(sys.argv) == 5):
        train_unsupervised(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit(usage)
