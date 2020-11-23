import tgalice

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)
from tgalice.dialog import Context, Response

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)


class DM(tgalice.dialog_manager.BaseDialogManager):
    def respond(self, ctx: Context):
        if not ctx.message_text:
            return Response('привет!')
        doc = Doc(ctx.message_text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        return Response('Леммы: ' + ' '.join([t.lemma for t in doc.tokens]))


connector = tgalice.dialog_connector.DialogConnector(
    dialog_manager=DM(),
)
server = tgalice.flask_server.FlaskServer(connector=connector)

if __name__ == '__main__':
    server.parse_args_and_run()