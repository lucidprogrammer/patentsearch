
# Project Overview

This project aims to search uspto patents data, to find patents similar to a given patent.

# Data
Refer to the [data approach](src/patentsearch/data/exploration/README.md)

# Project Status
## ETL
This stage of the project can be marked as 3.5/5 complete. We have normalised data. We have made
a [wrapper python class](src/patentsearch/data/patentsview/__init__.py) which can be used for direct population to PGSQL.
## Unsupervised learning
A sample is created with minimal tuning.Accuracy may not be great currently.
Refer to [get_similar](src/patentsearch/get_similar.ipynb)

To improve accuracy, one needs to do the following.
1. Create a validation procedure.
2. Create a cluster model, then a topic model and possibly within the existing patent classifications. One needs to iterate to see whats the best approach based on the specifics of the patent data as such.

# Development Environment

```
conda env create -f dev_env.yml

source activate patentsearch
```
