# Kvasir

[![Project Status: Unsupported – The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.](https://www.repostatus.org/badges/latest/unsupported.svg)](https://www.repostatus.org/#unsupported)
[![DOI](https://zenodo.org/badge/22309/kescobo/kvasir.svg)](https://zenodo.org/badge/latestdoi/22309/kescobo/kvasir)
[![Join the chat at https://gitter.im/kescobo/kvasir](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kescobo/kvasir?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Documentation Status](https://readthedocs.org/projects/kvasir/badge/?version=latest)](http://kvasir.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/kescobo/kvasir.svg?branch=master)](https://travis-ci.org/kescobo/kvasir)

Dependencies:
* Python 2.7 or 3.6
* MongoDB
  * pymongo
* BioPython
* Pandas (for dealing with distance matrices)
* BLAST+ CLI

**Identification of horizontal gene transfer between sequenced microbial genomes**

Kvasir takes as the input a folder containing genomes in genbank format. The
protein coding genes from these genomes are loaded into a database, and blasted
against each other.

[Kvasir](https://en.wikipedia.org/wiki/Kvasir) is a Norse god associated with
fermented beverages. According to Wikipedia,

>Extremely wise, Kvasir traveled far and wide, teaching and spreading knowledge.
This continued until the dwarfs Fjalar and Galar killed Kvasir and drained him
of his blood. The two mixed his blood with honey, resulting in the Mead of
Poetry, a mead which imbues the drinker with skaldship and wisdom, and the
spread of which eventually resulted in the introduction of poetry to mankind.

## Installation

The easiest way to use Kvasir is to install it from pypi:

```sh
$ pip install kvasirHGT
```

Take a look [at the docs](http://kvasir.readthedocs.io/en/latest/) for usage information.
