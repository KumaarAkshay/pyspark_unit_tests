# Run PySpark Locally on Windows & Run Pytest

## 1. Install Prerequisites

- Install Python.
- Install PySpark:

```powershell
pip install pyspark==3.5.6
```

- Install Pytest:

```powershell
pip install pytest
```

- Download and install Java JDK 17.

## 2. Configure Environment Variables

### JAVA_HOME

Set the Java installation directory:

```
JAVA_HOME = C:\Program Files\Java\jdk-17
```

Add to System `Path`:

```
%JAVA_HOME%\bin
```

**Note:** JAVA_HOME should point to the JDK folder, not its `bin` directory.

### HADOOP_HOME

- Download compatible Hadoop 3.x Windows binaries containing `winutils.exe` from [GitHub](https://github.com/cdarlint/winutils).
- Create the following directory structure:

```
C:\hadoop\bin\winutils.exe
```

Set the environment variable:

```
HADOOP_HOME = C:\hadoop
```

Add to System `Path`:

```
%HADOOP_HOME%\bin
```

## 3. Verify Environment Variables

### PowerShell Commands

```powershell
echo $env:JAVA_HOME
where.exe java
java -version

echo $env:HADOOP_HOME
where.exe winutils
```

### CMD Commands

```cmd
echo %JAVA_HOME%
where java
java -version

echo %HADOOP_HOME%
where winutils
```

**Note:** Restart VS Code after modifying environment variables.

## 4. Run a Sample PySpark Script

Create `main.py`:

```py
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("PySparkTest")
    .master("local[*]")
    .getOrCreate()
)

print("Spark Version:", spark.version)

data = [(1, "Akshay"), (2, "Rahul")]

df = spark.createDataFrame(data, ["id", "name"])
df.show()

spark.stop()
```

Run the script:

```powershell
python main.py
```

## 5. Run Pytest

Create `test_spark.py`:

```py
def test_addition():
    assert 2 + 3 == 5
```

Run all tests:

```powershell
pytest
```

Run with detailed output:

```powershell
pytest -v
```

Run a specific test file:

```powershell
pytest test_spark.py -v
```

## 1. How to Stop Spark Manually on Windows

### Option A: Using Task Manager

1. Press `Ctrl + Shift + Esc`.
2. Open the **Details** tab.
3. Look for `java.exe` or `python.exe`.
4. Identify the process associated with your Spark application.
5. Right-click → **End task**.

### Option B: Using PowerShell

Find running Java processes:

```powershell
Get-Process java
```

Terminate a specific Java process:

```powershell
Stop-Process -Id <PID> -Force
```

Find running Python processes:

```powershell
Get-Process python
```

Terminate a specific Python process:

```powershell
Stop-Process -Id <PID> -Force
```

**Note:** Replace `<PID>` with the actual process ID. Don't terminate all Java or Python processes blindly, as other applications may be using them.

Run Unit test

```powershell
pytest -v -s .\tests\test_read_bq_data_spark.py
```
