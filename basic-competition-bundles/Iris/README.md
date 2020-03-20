This is a more elaborate example with code OR result submission, using an ingestion program. It allows organizers to write a program that received Python classes (not executables) and call them on data loaded with a standard data loader (ehnce the participants do not have to read the input data themselves).

The example uses the well known Iris dataset from Fisher's classic paper (Fisher, 1936).. The data set contains 3 classes of 50 instances each, where each class refers to a type of iris plant. One class is linearly separable from the other 2; the latter are NOT linearly separable from each other.

References and credits: 

R. A. Fisher. The use of multiple measurements in taxonomic problems. Annual Eugenics, 7, Part II, 179-188 (1936). 
The competition protocol was designed by Isabelle Guyon. 
This challenge was generated using ChaLab for Codalab v1.5.

There are 2 phases:

* Phase 1: development phase. We provide you with labeled training data and unlabeled validation and test data. Make predictions for both datasets. However, you will receive feed-back on your performance on the validation set only. The performance of your LAST submission will be displayed on the leaderboard.

* Phase 2: final phase. You do not need to do anything. Your last submission of phase 1 will be automatically forwarded. Your performance on the test set will appear on the leaderboard when the organizers finish checking the submissions.

This sample competition allows you to submit either:

* Only prediction results (no code).
* A pre-trained prediction model.
* A prediction model that must be trained and tested.

NOTE: we provide the zipped and unzipped competition bundle for convenience. In the competition bundle, subdirectories should be zipped files (e.g scoring\_program). You can use the `make_competition_bundle.sh` script for that purpose:

```
cd iris_competition_bundle/utilities
./make_competition_bundle.sh
```

You can try your newly created competition by submitting one of those files into it:
```
sample_result_submission.zip
sample_code_submission.zip
```
