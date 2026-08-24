# Fault Detection in Lighthouse Photoresistor Sensor using Machine Learning and Many-Objective Optimisation

Code accompanying the paper *"Fault Detection in Lighthouse Photoresistor Sensor using Machine
Learning and Many-Objective Optimisation"*.

Lighthouses managed by the General Lighthouse Authorities (GLA) switch their main optic on and off
using a photoresistor that senses ambient light. Over time these sensors **drift**: the lamp starts
switching progressively earlier or later than the ambient light conditions warrant. Drift is gradual,
there is no ground-truth fault label, and a sensor can be substantially out before anyone notices.

The study covers 42 months of telemetry, June 2017 to December 2021, across 15 lighthouses.

This work treats drift detection as a by-product of a classification problem. A model is trained to
predict the sensor's state (`On` / `Off`) from weather and solar-geometry features at the moment of
each switching event. If the model is a faithful description of a *healthy* sensor, then feeding it
telemetry from a *drifted* sensor should make its accuracy fall — and fall **monotonically** as drift
grows. The rate of that fall becomes the detection signal.

The difficulty is that this behaviour is not automatic. Many feature subsets yield a model that is
accurate but insensitive to drift, or sensitive at one lighthouse and flat at another. Finding a
subset that degrades cleanly *at every lighthouse simultaneously* is a many-objective problem, and
that is what the NSGA-III stage solves.

---

## How the pieces fit together

The pipeline runs in four stages. Each stage consumes the previous stage's output.

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │ 1. PREPROCESSING                              1_preprocessing/      │
   │                                                                     │
   │   raw telemetry (.xlsx)          ERA5 + CAMS climate/solar          │
   │      │  process_telemetry_data_*.py    │  get_climate_data.py       │
   │      ▼                                 ▼                            │
   │   clean On/Off events  ───── Merging.py ─────►  merged per-station  │
   │   + sun angle           (interpolate hourly       1-minute datasets │
   │                          climate to event time,                     │
   │                          add pvlib solar geometry)                  │
   │                                 │                                   │
   │                                 ▼  add_MA.py  (2-step moving avgs)  │
   │                                 ▼  create_merged_datasets.py        │
   │                          leave-one-lighthouse-out "global" datasets │
   └─────────────────────────────────┬───────────────────────────────────┘
                                     │
   ┌─────────────────────────────────▼───────────────────────────────────┐
   │ 2. BASELINE CLASSIFICATION + DRIFT RESPONSE   2_classification/     │
   │                                                                     │
   │   Eight algorithms, grid-searched, 10-fold CV:                      │
   │   DT · RF · XGBoost · KNN · MLP · SVC · AdaBoost · LogReg           │
   │                     drifted_analysis.py                             │
   │                                                                     │
   │   Each trained model is then applied to the same lighthouse's       │
   │   drifted telemetry at ±1, 5, 10, 15, 20, 25, 30 minutes            │
   │                     create_test_set.py  (builds the X/y test sets)  │
   └─────────────────────────────────┬───────────────────────────────────┘
                                     │  accuracy-vs-drift curve
                                     │  per lighthouse
   ┌─────────────────────────────────▼───────────────────────────────────┐
   │ 3. MANY-OBJECTIVE FEATURE SELECTION           3_nsga3/              │
   │                                                                     │
   │   Chromosome = binary mask over the feature set                     │
   │   Objective k = slope of lighthouse k's accuracy-vs-drift curve     │
   │                 (minimised: steeper negative slope = better)        │
   │                                                                     │
   │             NSGA3_DEAP.py  ──calls──►  drifted_analysis_for_GA.py   │
   │                                        (.check_drifting(chromosome))│
   └─────────────────────────────────┬───────────────────────────────────┘
                                     │  Pareto front
   ┌─────────────────────────────────▼───────────────────────────────────┐
   │ 4. RESULTS ANALYSIS                           4_analysis/           │
   │   Filter the front, count feature occurrences, produce the figures  │
   └─────────────────────────────────────────────────────────────────────┘
```

The key coupling is between stages 3 and 2: **NSGA-III does not optimise classification accuracy.**
Its fitness function retrains an MLP and re-runs the whole drift evaluation for every candidate
feature subset, then returns one slope per lighthouse. This is why a single evolutionary run is
expensive and was executed on a compute cluster.

### The two lighthouse groups

Models are trained *globally* per group rather than per lighthouse, using a leave-one-out scheme
(`create_merged_datasets.py`) analogous to k-fold cross-validation: to build the training set for
lighthouse *i*, the datasets of all **other** lighthouses in the group are merged, and lighthouse
*i*'s own drifted data becomes the test set. This tests whether drift detection generalises to a
lighthouse the model has never seen.

| Group | Lighthouses | Objectives |
|---|---|---|
| **NLB** (Northern Lighthouse Board) | Balta Sound, Dunnet Head, Flotta Grinds Buoy, Mousa, North Rona, North Ronaldsay, Sule Skerry, Sumburgh Head | 8 |
| **TH** (Trinity House) | Bishop Rock, Eddystone, Godrevy, Lizard, Longships, Trevose, Wolf Rock | 7 |

With the optional `first_values` objectives enabled (which additionally reward a high *starting*
accuracy, so the search cannot win by picking a model that is uniformly terrible), the objective
count doubles to **16** for NLB and **14** for TH.

### Features

28 features in total — 17 base plus 11 two-step moving averages — giving the 2^28 feature
combinations the paper's search space refers to:

- **Weather** (ERA5): `Temp2m`, `Dewpoint2m`, `Pressure`, `Precipitation`
- **Irradiance** (CAMS, observed-cloud): `GHI_N`, `DHI_N`, `BNI_N`
- **Solar geometry** (`pvlib`, clear-sky Ineichen): `zenith`, `elevation`, `azimuth`,
  `equation_of_time`, `ghi_M`, `dhi_M`, `dni_M`, plus `Sunangle` from `ephem`
- **Moving averages**: a 2-step rolling mean of each of the above, capturing how conditions changed
  across an adjacent On/Off pair

`apparent_zenith` and `apparent_elevation` are present in the merged data but were found to be
numerically identical to `zenith` / `elevation` and are excluded from the search.

---

## Repository layout

```
1_preprocessing/
    process_telemetry_data_NLB.py      Clean raw NLB telemetry; drop consecutive
                                       duplicate states and spurious short On-Off
                                       pairs (<20 min); compute sun angle
    process_telemetry_data_TH.py       Same for Trinity House (differs: local-time
                                       to UTC conversion, different column schema)
    process_telemetry_data_drifted.py  Same for the pre-drifted telemetry files
    run_all_NLB.sh, run_all_TH.sh      Batch drivers; carry each station's lat/lon
    get_climate_data.py                Download ERA5 weather + CAMS solar, combine,
                                       interpolate to a common time index
    Merging.py                         Merge telemetry with climate; interpolate the
                                       hourly climate values to each event's exact
                                       time; append pvlib solar features
    add_MA.py                          Add the 2-step moving-average features
    create_merged_datasets.py          Leave-one-lighthouse-out merged datasets

2_classification/
    drifted_analysis.py                Main baseline: 8 algorithms x grid search x
                                       10-fold CV, then drift evaluation
    drifted_analysis_dynamic_features.py
                                       As above but sweeping feature subsets
                                       exhaustively (the pre-NSGA-III approach)
    create_test_set.py                 Build scaled X/y test sets over 100% of a
                                       drifted dataset (no train/test split)

3_nsga3/
    NSGA3_DEAP.py                      NSGA-III driver (DEAP). Objective count is
                                       derived from the station argument
    drifted_analysis_for_GA.py         Fitness function: check_drifting(chromosome)
                                       returns one slope per lighthouse
    GLA.py                             Cluster entry point
    run.sh                             Sun Grid Engine submission script
    exhaustive_baseline/               Brute-force enumeration of feature subsets,
                                       used as the comparison baseline (NLB/TH,
                                       plus chunked variants for parallel jobs)

4_analysis/
    CERES_analysis_EA2.py              Filter exhaustive-search output by slope
    CERES_analysis_EA3456.py           Filter and deduplicate the NSGA-III Pareto
                                       fronts across runs
    best_features.txt                  Accuracy tables for the feature subsets that
                                       produced correct drift behaviour

notebooks/
    GLA-Phase3.ipynb                   Exploratory analysis (correlation, mutual
                                       information, normality tests, box plots) and
                                       the figure-generating cells

figures/                               Figures as they appear in the paper
```

---

## Running it

### Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Data

**No data is included in this repository.** The GLA telemetry is not ours to redistribute; enquiries
should be directed to the General Lighthouse Authorities. The climate and solar inputs are freely
available and reproducible with `get_climate_data.py` given a Copernicus account.

### Path configuration — read this first

These scripts were written to run from a project root that held the data alongside the code, and
they configure their I/O through module-level `path` / `input` / `input2` / `results` variables near
the top of each file rather than through command-line arguments. Because the data directories are not
shipped here, **you must edit those variables to point at your own data root before running any
stage.** For example, in `2_classification/drifted_analysis.py`:

```python
path    = './'
input   = 'Merged datasets/NLB_merged/1-min/moving_averages/'
input2  = 'NLB/drifted/x-y test sets/1-min/moving_averages/'
results = 'results-temp/classification/'
```

Switching a script between the NLB and TH groups is done the same way, by editing these paths.

### Stage 1 — preprocessing

```bash
python 1_preprocessing/get_climate_data.py --name=Mousa --latitude=59.997567 --longitude=-1.158433 --startDate=2017-01-01 --endDate=2021-12-31
```

`get_climate_data.py` reads its Copernicus credentials from the environment — nothing is stored in
the repository:

```bash
export CDSAPI_KEY='<uid>:<your-cds-api-key>'    # cds.climate.copernicus.eu
export ADSAPI_KEY='<uid>:<your-ads-api-key>'    # ads.atmosphere.copernicus.eu
```

The two stores are separate services requiring separate registrations. Then:

```bash
bash 1_preprocessing/run_all_NLB.sh            # clean telemetry, compute sun angle
python 1_preprocessing/Merging.py True True False   # args: nlb, clean, drifted
python 1_preprocessing/add_MA.py
python 1_preprocessing/create_merged_datasets.py
```

`Merging.py` takes three positional booleans: `nlb` (True = NLB, False = TH), `clean` (use
cleaned telemetry), and `drifted` (process the drifted rather than the healthy datasets).

### Stage 2 — baseline classification and drift response

```bash
python 2_classification/create_test_set.py     # X/y test sets for the drifted data
python 2_classification/drifted_analysis.py
```

Fixed experimental settings: `seed=100`, 10-fold cross-validation, a 0.25 test split, and
`n_jobs=50` for grid search — **lower `njobs` to suit your machine.** Drift experiments performed
better on unscaled data, so scaling is deliberately bypassed in the drift path; the relevant lines
are commented in place rather than deleted.

### Stage 3 — NSGA-III feature selection

```bash
cd 3_nsga3
python NSGA3_DEAP.py NLB True                  # station: NLB|TH, first_values: True|False
```

On a Sun Grid Engine cluster, `qsub run.sh NLB True`.

### Search parameters

The published configuration is the one reported in Section 4 of the paper, obtained by grid search
and compared across configurations with a Friedman test:

| Parameter | Published value |
|---|---|
| Population | **300** |
| Generations | **35** |
| Crossover rate | **0.9** |
| Mutation rate | **0.1** |
| Selection | `selNSGA3` |
| Reference points | two-layer, `P = [5, 4]`, `SCALES = [1, 0.5]` |
| Objectives | 8 (NLB) / 7 (TH); 16 / 14 with `first_values` enabled |

> **The scripts in this repository are set to other values.** `NSGA3_DEAP.py` as committed carries
> the settings of a *different* experimental run — 50 generations, crossover 0.85, mutation 0.15,
> and a population derived from the reference-point count rather than fixed at 300. The scripts are
> published in that state because that is how those experiments were run; they have not been
> back-edited. **To reproduce the paper, set the four values above** at the top of
> `3_nsga3/NSGA3_DEAP.py`:
>
> ```python
> MU = LAMBDA = 300   # replace: MU = int(H + (4 - H % 4))
> NGEN  = 35          # replace: 50
> CXPB  = 0.9         # replace: .85
> MUTPB = 0.1         # replace: .15
> ```

The inner classifier is an MLP. Four configurations were run; they differ **only** in these two
hyperparameters. `3_nsga3/drifted_analysis_for_GA.py` ships as the EA6 configuration — reproduce any
other by editing `set_params()`:

| Configuration | `hidden_layer_sizes` | `max_iter` |
|---|---|---|
| EA3 | `4` | `2000` |
| EA4 | `len(features_all) + 1` | `2000` |
| EA5 | `len(features_all) + 1` | `1000` |
| **EA6** (as shipped) | `len(features_all) + 1` | `200` |

The exhaustive baseline that EA2 corresponds to lives in `3_nsga3/exhaustive_baseline/`.

### Stage 4 — analysis

```bash
python 4_analysis/CERES_analysis_EA3456.py
```

Both analysis scripts read the evolutionary run logs by path (`./CERES_results/EA*/Tasks/*.txt`).
Those logs are ~19 MB of raw output derived from GLA data and are **not** included here — see below.

---

## Known gaps

Stated plainly, so nobody loses time on them:

1. **`GLA.py` depends on an EA/GA framework that is not in this repository.** It imports `EA` and
   `GA`, a separate in-house evolutionary-computation library that lived alongside the code on the
   cluster. `GLA.py` therefore will not run standalone. It is included because it documents the
   exact search configuration used. Point `EA_FRAMEWORK_PATH` at a checkout if you have one.
   `NSGA3_DEAP.py`, which is the NSGA-III implementation the paper reports, depends only on DEAP and
   runs without it.
2. **Evolutionary run logs are not included.** `CERES_analysis_EA2.py` and `CERES_analysis_EA3456.py`
   parse `NLB_*.txt` / `TH_*.txt` output files that are not published here. Regenerate them by
   running stage 3, or request them from the authors.
3. **`pymop` is unmaintained.** `NSGA3_DEAP.py` uses it only for the `Problem` base class. It has
   been superseded by [pymoo](https://pymoo.org); a port is a small change but has not been made,
   since the published results were produced with `pymop` 0.2.4.
4. **The drift injection itself is upstream of this code.** The drifted telemetry arrived as files
   carrying a `Drift Minutes` column; `process_telemetry_data_drifted.py` consumes and cleans them
   rather than generating the offsets.
5. **Notebook outputs have been cleared** to keep dataset rows out of the repository. Cells must be
   re-executed against your own data.

---

## Citation

> Dost, S., Christodoulaki, E., Vastardis, N., & Kampouridis, M. Fault Detection in Lighthouse
> Photoresistor Sensor using Machine Learning and Many-Objective Optimisation.

*(Volume, pages and DOI to be completed on publication.)*

## Data availability

The lighthouse telemetry underlying this study was provided by the General Lighthouse Authorities
and is not publicly redistributable. The climate and solar inputs are derived from the Copernicus
ERA5 reanalysis and CAMS solar radiation service, both openly available, and can be regenerated with
`1_preprocessing/get_climate_data.py`.

## Licence

Released under the MIT Licence — see [LICENSE](LICENSE).
