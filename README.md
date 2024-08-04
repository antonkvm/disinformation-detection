# Disinformation Detection Pipeline

## Setup

To not clog up the global Python package installations, set up a virtual environment:

~~~Shell
# build virtual environment folder 'venv'
python -m venv venv

# activate venv (might differ depending on OS)
source venv/bin/activate

 # install dependencies into venv
 # (includes spacy's ~550MB 'en-core-web-lg' model)
pip install -r requirements.txt 

# for jupyter notebook: install kernel from the active venv onto your machine
# (this will make a kernel 'venv_ddp' available that has the dependencies installed)
ipython kernel install --user --name=venv_ddp

# uninstall the kernel with
jupyter-kernelspec uninstall venv_ddp

# if you forgot the kernel name, you can list installed kernels with
jupyter-kernelspec list
~~~

## Notes for later

When processing multiple sentences into spacy's nlp method, don't do it in a loop but rather use the pipe method:

~~~Python
texts = ["This is a text", "These are lots of texts", "..."]
docs = [nlp(text) for text in texts]  # bad
docs = list(nlp.pipe(texts))  # good
~~~
