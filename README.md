# Disinformation Detection Pipeline

## Setup

Set up a virtual environment to not clog up the global Python package installation folder:

1. Build a virtual environment folder called 'env':

    ~~~zsh
    python -m venv env
    ~~~

2. Activate the environment (might differ depending on OS):

    ~~~zsh
    source env/bin/activate
    ~~~

3. Install the dependencies into your venv:

    ~~~zsh
    pip install -r requirements.txt 
    ~~~

4. For Jupyter Notebook: make the virtual environment available as a kernel:

    ~~~zsh
    ipython kernel install --user --name=venv_ddp
    ~~~

5. If needed, uninstall the kernel with:

    ~~~zsh
    jupyter-kernelspec uninstall venv_ddp
    ~~~

6. If you forgot the kernel name, you can list installed kernels with

    ~~~zsh
    jupyter-kernelspec list
    ~~~

## Usage

~~~Python
import knowledge_extractor as knex

text = 'Obama was born in Hawaii.'
triples = knex.extract_spo_triples(text)
print(triples)
~~~

Output:

~~~Python
[SPO_triple(subject='Barack Obama', predicate='born in', object='Hawaii')]
~~~

## Notes for later

When processing multiple sentences into spacy's nlp method, don't do it in a loop but rather use the pipe method:

~~~Python
texts = ["This is a text", "These are lots of texts", "..."]
docs = [nlp(text) for text in texts]  # bad
docs = list(nlp.pipe(texts))  # good
~~~
