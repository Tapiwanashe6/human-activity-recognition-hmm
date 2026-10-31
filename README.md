# Human Activity Recognition Using Hidden Markov Models

Individual Machine Learning Techniques II assignment by **Tapiwanashe Gift Marufu**.

This project recognizes **standing, walking, still, and jumping** from smartphone acceleration and gyroscope data. It implements Gaussian HMM emissions, log-space forward–backward, regularized Baum–Welch, and Viterbi using NumPy.

[Open the notebook in Google Colab](https://colab.research.google.com/github/Tapiwanashe6/human-activity-recognition-hmm/blob/main/Human_Activity_HMM.ipynb)

## Results and scope

| Evaluation | Recordings | Feature windows | Viterbi accuracy | Emission-only accuracy |
|---|---:|---:|---:|---:|
| Validation | 10 | 71 | 100% | 100% |
| Separate labelled tests | 4 | 28 | 100% | 100% |

These results concern one participant and one phone. Windows overlap and are correlated; they are not 28 independent test trials. There was no measured accuracy benefit from Viterbi in these labelled tests. A separate continuous recording demonstrates predicted switches and phone-handling ambiguity, but lacks independently timed labels and is **not scored for accuracy**.

## Dataset and preprocessing

- **50 cleaned development CSVs:** 13 standing, 13 walking, 12 still, 12 jumping.
- Every cleaned development recording lasts 5–10 seconds; every activity retains at least 90 seconds in total.
- Whole recordings are split into **40 training and 10 validation files** before windowing.
- **Four additional labelled test files**, one per activity, remain separate.
- One additional continuous recording is used for qualitative analysis only.
- Data were collected individually at ALU Soules B Residence using an SM-M346B Android phone and Sensor Logger 1.68.
- Measured sampling is about 49.876 Hz, aligned to a common 50 Hz grid.
- Standard boundary trims are 0.3 seconds at each end; development still recording 4 has a documented 1.0-second end trim.
- Windows are 2 seconds with a 1-second step. Three time-domain and two FFT-derived features use training-fitted log/Z-score transforms.
- Raw metadata device identifiers are blanked in the published input ZIPs; measurement values are unchanged. Original local recordings are preserved.

### Cleaned CSV schema

`timestamp_ns, seconds_elapsed, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, activity, recording_id`

Acceleration is in m/s² and rotation in rad/s. Reconstructed timestamps refer to the common interpolated grid. The continuous cleaned file intentionally has no ground-truth activity labels.

## Repository layout

```text
Human_Activity_HMM.ipynb       Executed notebook and explanations
inputs/                      Three input ZIPs required for a fresh run
data/cleaned/                Exactly 50 cleaned development CSVs
data/test_cleaned/           Four separate labelled test CSVs
data/continuous_cleaned.csv  Continuous recording without timed ground truth
data/*manifest.csv           Recording split and window provenance
models/                      Fitted HMM and preprocessing parameters
results/                     Audit tables, metrics, predictions, convergence
figures/                     Notebook-generated figures
report/                      Five-page Word report
scripts/run_notebook.py      Fresh local sequential execution helper
requirements.txt             Analysis dependencies
```

## Run in Colab

1. Open the notebook using the link above and save a copy if you want to edit it.
2. Download these files from `inputs/` and upload them into Colab session storage (`/content`):
   - `Human_Activity_Recordings.zip`
   - `Test_Recordings.zip`
   - `Continuous_Recording.zip`
3. Choose **Runtime → Restart session and run all**.
4. The notebook creates `/content/activity_hmm` and downloads a project backup in its last cell.

Expected checks: 50 cleaned files, convergence after three updates, 71/71 validation windows and 28/28 test windows correct. Input filenames matter. Colab session storage is temporary.

## Run locally

Use Python 3.10 or later and install the dependencies in an environment of your choice:

```bash
python -m pip install -r requirements.txt
python scripts/run_notebook.py
```

The helper executes the analysis cells in a fresh namespace, adapting `/content` to the ignored `.run/` directory and skipping only the Colab-specific download cell. It preserves the notebook source and regenerates outputs under `.run/activity_hmm`. A fresh local verification used NumPy 2.4.6, pandas 3.0.3, and Matplotlib 3.10.9.

## Methods and limitations

Recordings remain independent sequences, so no transitions are invented between shuffled files. Initial means use training labels to preserve state identities; training is therefore not entirely unsupervised. Transition pseudocounts regularize switching estimates because training clips contain single activities. Convergence monitors the regularized objective and flags significant decreases. A synthetic exhaustive-path example checks likelihood, posteriors, expected transitions, and Viterbi.

The report discusses single-participant/device limits, correlated features and overlapping windows, the absence of timed transition ground truth, and handling-related ambiguity. Do not interpret near-perfect clip recognition as proven generalization to other people or environments.

## Submission status

The notebook, dataset, report, and repository are present. **Four activity-video links still need to be added to the report before submission.** The report contains an explicit placeholder for each. Videos must meet the assignment's identity, lighting, full-body and activity requirements.

## References

- [Sensor Logger official units](https://github.com/tszheichoi/awesome-sensor-logger/blob/main/UNITS.md)
- [Rabiner (1989), A tutorial on hidden Markov models](https://doi.org/10.1109/5.18626)
