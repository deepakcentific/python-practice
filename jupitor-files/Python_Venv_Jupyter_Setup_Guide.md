# Python + venv + JupyterLab Setup Guide (Windows)

## One-Time Installation

### Verify Python

```powershell
python --version
pip --version
```

### Install Jupyter and ipykernel

```powershell
pip install jupyterlab ipykernel
```

---

# Create a New Python Project

## 1. Create a project folder

```powershell
mkdir my-project
cd my-project
```

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

## 3. Activate the virtual environment

If PowerShell blocks scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Expected prompt:

```text
(.venv) PS C:\path	o\my-project>
```

## 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

## 5. Install required packages

Example:

```powershell
pip install requests pandas matplotlib numpy ipykernel jupyterlab
```

## 6. Save dependencies

```powershell
pip freeze > requirements.txt
```

---

# Setup Jupyter Kernel for the Project

Register the virtual environment as a kernel:

```powershell
python -m ipykernel install --user --name=my-project --display-name "Python (my-project)"
```

Start JupyterLab:

```powershell
jupyter lab
```

Or:

```powershell
jupyter notebook
```

Select:

```text
Python (my-project)
```

as the active kernel.

---

# Reopen the Project Later

Navigate to your project:

```powershell
cd C:\path	o\my-project
```

Activate venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Jupyter:

```powershell
jupyter lab
```

---

# Install Dependencies on Another Machine

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

# Useful Commands

### Show installed packages

```powershell
pip list
```

### Check active Python interpreter

```powershell
where python
```

Expected output:

```text
...\my-project\.venv\Scripts\python.exe
```

### List Jupyter kernels

```powershell
jupyter kernelspec list
```

### Deactivate virtual environment

```powershell
deactivate
```

---

# Recommended DevOps Learning Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install requests pandas pyyaml jupyterlab ipykernel
python -m ipykernel install --user --name=my-project --display-name "Python (my-project)"
jupyter lab
```

## Notes

- Anaconda is NOT required.
- Python + venv + JupyterLab is sufficient.
- Ideal for DevOps, Kubernetes, Azure automation, APIs, and scripting.
- Use a separate `.venv` for each project.
