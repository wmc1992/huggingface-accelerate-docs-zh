# Installation

🤗 Accelerate is tested on Python 3.6+, and PyTorch 1.6.0+.

You should install 🤗 Accelerate in a virtual environment. If you’re unfamiliar with Python virtual environments, check out the user guide. Create a virtual environment with the version of Python you’re going to use and activate it.

Now, if you want to use 🤗 Accelerate, you can install it with pip.

## Installation with pip

First you need to install PyTorch. Please refer to the PyTorch installation page regarding the specific install command for your platform.

When PyTorch has been installed, 🤗 Accelerate can be installed using pip as follows:


```
pip install accelerate
```

Alternatively, for CPU-support only, you can install 🤗 Accelerate and PyTorch in one line with:

```
pip install accelerate[torch]
```

To check 🤗 Accelerate is properly installed, run the following command:

```
python -c "TODO write"
```

## Installing from source

Here is how to quickly install accelerate from source:

pip install git+https://github.com/huggingface/accelerate
Note that this will install not the latest released version, but the bleeding edge master version, which you may want to use in case a bug has been fixed since the last official release and a new release hasn’t been yet rolled out.

While we strive to keep master operational at all times, if you notice some issues, they usually get fixed within a few hours or a day and and you’re more than welcome to help us detect any problems by opening an Issue and this way, things will get fixed even sooner.

Again, you can run:

```
python -c "TODO write"
```

to check 🤗 Accelerate is properly installed.

## Editable install

If you want to constantly use the bleeding edge master version of the source code, or if you want to contribute to the library and need to test the changes in the code you’re making, you will need an editable install. This is done by cloning the repository and installing with the following commands:

```
git clone https://github.com/huggingface/accelerate.git
cd transformers
pip install -e .
```

This command performs a magical link between the folder you cloned the repository to and your python library paths, and it’ll look inside this folder in addition to the normal library-wide paths. So if normally your python packages get installed into:

```
~/anaconda3/envs/main/lib/python3.7/site-packages/
```

now this editable install will reside where you clone the folder to, e.g. ~/accelerate/ and python will search it too.

Do note that you have to keep that accelerate folder around and not delete it to continue using the 🤗 Accelerate library.

Now, let’s get to the real benefit of this installation approach. Say, you saw some new feature has been just committed into master. If you have already performed all the steps above, to update your accelerate repo to include all the latest commits, all you need to do is to cd into that cloned repository folder and update the clone to the latest version:

```
cd ~/accelerate/
git pull
```

There is nothing else to do. Your python environment will find the bleeding edge version of 🤗 Accelerate on the next run.
