# MgK-pred

MgK-pred is a machine learning-based framework for validating and predicting Mg<sup>2+</sup> and K<sup>+</sup> ions in experimentally resolved biomolecular structures.

The method uses graph-based structural signatures combined with atomic element descriptors to represent the ion-binding environment. These signatures are used as input for a Multilayer Perceptron (MLP) neural network trained to distinguish Mg<sup>2+</sup> and K<sup>+</sup> coordination sites.

Our best model achieved accuracy values above 96% on independent test datasets.

---

# Overview

Correct annotation of metal ions in experimentally resolved structures is essential for structural biology, molecular modeling, and bioinformatics analyses. However, distinguishing Mg<sup>2+</sup> and K<sup>+</sup> ions remains challenging due to similarities in electron density and limitations in experimental resolution.

MgK-pred was developed to assist the validation of these ions using machine learning and structural bioinformatics approaches.

The workflow consists of:

1. Extraction of ion coordination environments from biomolecular structures;
2. Construction of graph-based structural signatures (using <a href="https://github.com/LBS-UFMG/signa">SIGNA</a>);
3. Encoding of atomic and physicochemical information;
4. Training and evaluation of MLP neural network models using Orange Data Mining;
5. Prediction of Mg<sup>2+</sup> and K<sup>+</sup> ion identities.

---

# Repository Structure

```text
MgK-pred/
│
├── structural-signatures/  # Training and test datasets
├── binding-sites/          # CIF/PDB files for each ion (6 Å zone)
├── models/                 # Trained machine learning models (Orange files)
├── scripts/                # Python scripts used in preprocessing
├── comparison/             # Data used for comparisons
├── structures/             # PDB/CIF files
└── README.md
```

---

# Methodology

The proposed approach represents ion-binding sites using graph-based structural signatures.

For each ion environment:

* atoms are represented according to their atomic elements;
* interatomic contacts are encoded as graph relationships;
* descriptors capture the spatial and physicochemical organization of the coordination site.

The resulting feature vectors are used as input for machine learning classification.

The models were evaluated using independent test datasets and manually curated ribosomal structures.

---

# Requirements

The project was developed using Python 3.

Main dependencies include:

```bash
Orange Data Mining
```

---

# Running the Models

Models must be tested using Orange Data Mining interface.

---

# Dataset

The datasets used in this study were constructed from experimentally resolved biomolecular structures containing Mg<sup>2+</sup> and K<sup>+</sup> ions.

The repository includes:

* training datasets;
* independent test datasets;
* prediction examples;
* manually curated case studies.

---

# Results

Our best MLP model achieved:

| Metric                      | Value      |
| --------------------------- | ---------- |
| Accuracy                    | >96%       |
| Independent Test Evaluation | Successful |

The model was also evaluated on manually curated *E. coli* ribosome structures and successfully identified several ions later corrected in updated structural annotations.

---

# Citation

If you use MgK-pred in your research, please cite:

```bibtex
@article{MgKPred2026,
  title={Machine learning-based validation of Mg2+ and K+ ions using graph-based structural signatures},
  author={Diego Mariano},
  journal={not published yet},
  year={2026}
}
```

---

# License

This project is distributed under the MIT License.

---

# Authors

Developed by the Laboratory of Bioinformatics and Systems (LBS-UFMG).

GitHub organization:
https://github.com/LBS-UFMG
