# FAHP_eval

## Setup

Clone the project repository:
```bash
git clone https://github.com/thuCGRA/FAHP_eval.git
```

## Usage

### Configuration

* *chiplets.json*: serves as a chiplet library, containing detailed information about various chiplets, including their types (such as computing, memory, interconnect), process nodes (e.g., 7nm, 14nm), and performance parameters (e.g., computing speed, storage capacity, power consumption)
* *SiP_configuration.json*: provides the configuration details of the multi-chiplet systems
* *development_info.json*: contains preference settings of the designers and other important parameters

### Run evaluation

#### Run evaluation in test mode:

```bash
python fuzzy_eval.py -test
```

Number of solutions can be modified here in *fuzzy_eval.py*:

```python
terminal_metrics=tm.generate_terminal_metrics(TEST_MODE = True if '-test' in sys.argv else False, n_solutions_TEST=10)
```

#### Run evaluation for case study(Standardization of D2D interconnects):

```bash
python fuzzy_eval.py -standard
```

#### Run evaluation in normal mode:

```bash
python fuzzy_eval.py
```

## Contact

Do you have any questions? Contact us at THU_CGRA@163.com.


