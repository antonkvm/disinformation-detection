"""Extract the knowledge in a text as Subject-Predicate-Object Triples.

This module exposes one function: `extract_spo_triples`, which is to be called with a string argument `text`.

Returns a list of SPO-triples found in `text`.

The triples are named tuples with properties `subjects`, `predicate` and `object`.
"""

from collections import namedtuple

import spacy
from spacy.tokens import Doc, Span, Token

SPO_triple = namedtuple('SPO_triple', ['subject', 'predicate', 'object'])

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')


def extract_spo_triples(text: str) -> list[SPO_triple]:
    """Extract the knowledge from `text` as SPO-triples.

    Args:
        text (str): The input text to extract knowledge from.

    Returns:
        list[SPO_triple]: A list of named tuples containing the SPO-triples.
    """
    doc = nlp(text)
    triples = []
    for sent in doc.sents:
        predicates = _get_predicates(sent)
        for p in predicates:
            subjects_for_predicate = _get_subjects_for_predicate(p, sent)
            for s in subjects_for_predicate:
                objects_for_predicate = _get_objects(sent)
                for o in objects_for_predicate:
                    # save modified variables as to not tamper with lists during looping:
                    s_ = _expand_noun_chunk(s, doc)
                    p_ = _expand_verb_modifiers(p, doc)
                    o_ = _expand_noun_chunk(o, doc)
                    triples.append(SPO_triple(s_, p_, o_))
    return triples


# TODO: this only extracts one predicate, but a sentence could include multiple.
def _get_predicates(sent: Span) -> list[Token]:
    root = [token for token in sent if token.head == token][0]
    root_conjuncts = [token for token in sent if root in token.conjuncts]
    return [root] + root_conjuncts


def _get_subjects_for_predicate(predicate: Token, sent: Span) -> list[Token]:
    """Return a list of subject tokens in `sent` associated with `predicate`."""
    subjects_for_predicate = []
    p = predicate
    for token in sent:
        if ('subj' in token.dep_ and token.head == p) or p in [t.head for t in token.conjuncts if 'subj' in t.dep_]:
            subjects_for_predicate.append(token)
    return subjects_for_predicate


# TODO: long multi-word objects get split into multiple objects
def _get_objects(sent: Span) -> list[Token]:
    obj_dep_types = ['pobj', 'dobj', 'acomp', 'attr', 'oprd']  # might be incomplete: add advcl, auxpass?
    direct_objects = [t for t in sent if t.dep_ in obj_dep_types]
    object_conjuncts = [t for d_obj in direct_objects for t in sent if t in d_obj.conjuncts]
    return direct_objects + object_conjuncts


def _expand_noun_chunk(noun: Token, doc: Doc) -> str:
    """Expand `token` to its containing noun chunk in `doc`, if it exists. Otherwise return `token`."""
    for chunk in doc.noun_chunks:
        if noun in chunk:
            return chunk.text


def _expand_verb_modifiers(verb: Token, doc: Doc) -> str:
    """Expand a single token `verb` with connected verb modifiers in `doc`."""
    verbmod_deptypes = ['advmod', 'neg', 'prep', 'prt', 'agent']  # add dep labels as needed, 'aux'?
    modifiers = [t for t in doc if t.head == verb and t.dep_ in verbmod_deptypes]
    lefts = [t for t in modifiers if t in verb.lefts]
    rights = [t for t in modifiers if t in verb.rights]
    full_verb = lefts + [verb] + rights
    return ' '.join([t.text for t in full_verb])


if __name__ == '__main__':
    text = 'The great barrier reef is endangered by climate change. Obama was born in Hawaii.'
    print('Extracting triples from example sentence:\n', text)
    knowledge = extract_spo_triples(text)
    print('Extracted SPO-triples:')
    for i, triple in enumerate(knowledge):
        print(i + 1, ': ', triple, sep='')
