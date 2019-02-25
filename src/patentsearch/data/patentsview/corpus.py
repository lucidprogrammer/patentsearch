from gensim.models.doc2vec import TaggedDocument
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
import pandas as pd
from . import metadata
from . import PatentsView
import sys


class PatentsViewTaggedDocument(object):
    '''
    Create a reusable class which efficiently create tagged documents with very
    low overhead. You must have ideally downloaded the required datafile from
    patentsview before using this.
    This accepts either the zip file directly or the unzipped tsv file.
    If you do not provide the tsv_or_tsvzip parameter, this will auto download.
    (use that option in continuous ingestion mode.)

    '''

    def __init__(
            self,
            dataset_name: str,
            tsv_or_tsvzip: str = None,
            required_docs_count=1000):
        pv = PatentsView()
        if(dataset_name not in pv.available_data):
            raise ValueError(
                '%s is not a valid dataset name in patentsview'
                % dataset_name)
        dataset = metadata.data.get(dataset_name)
        if(not dataset):
            raise ValueError(
                'metadata for %s \
                is not in metadata.py' %
                dataset_name)
        text_field = dataset.get('text_field')
        id_field = dataset.get('id_field')

        if(not text_field or not id_field):
            raise ValueError(
                'incorrect metadata provided without text_field and id_field.\
                for %s ' % dataset_name)
        if(not tsv_or_tsvzip):
            tsv_or_tsvzip = pv.__dict__.get(dataset_name).get('url')
            sys.stderr.write('\n Using the tsv zip url directly. \
            It will download and do the training. Use this only in batch mode \
            for data ingestion')
        self.reader = pd.read_csv(
            tsv_or_tsvzip,
            delimiter='\t',
            iterator=True,
            compression='infer')
        self.required_docs_count = required_docs_count
        self.max_docs_count = pv.__dict__.get(dataset_name).get('rows')
        self.current_docs_count = 0
        self.text_field = text_field
        self.id_field = id_field

    def __iter__(self):

        while self.current_docs_count < self.required_docs_count and \
                self.current_docs_count < self.max_docs_count:
            chunk = self.reader.get_chunk(1)
            print(chunk)
            raw_text = chunk.iloc[0].get(self.text_field)
            id = chunk.iloc[0].get(self.id_field)
            sys.stderr.write('%d - %s\n' % (self.current_docs_count, str(id)))
            pre_processed_document_tokens = preprocess_string(
                remove_stopwords(raw_text))
            self.current_docs_count += 1
            yield TaggedDocument(pre_processed_document_tokens, [str(id)])
