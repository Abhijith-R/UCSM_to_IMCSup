# UCS Manager to IMC Supervisor 
This solution aims to migrate configuration from UCS Manager (e.g. service profiles) to IMC Supervisor and applies those
configurations to UCS-C series
 
## Source installation

In order to run this in your environment follow these steps:

1) Clone repo

```bash
git clone https://wwwin-github.cisco.com/gve/UCSM_to_IMCSup.git
```

2) Within the root directory of the application, install pip dependencies (use a virtual environment when possible)

```bash
pip install -r requirements.txt
```

3) Run the main file

```bash
python run.py
```
