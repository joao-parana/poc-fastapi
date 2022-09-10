# TPC-H Test data for IBIS, PyArrow e Pandas using Parquet

Example:

```python
import os
import pandas as pd
import pyarrow as pa
os.system('ls -lA parquet/tpch_lineitem/')
d = 'parquet/tpch_lineitem/'
pd.options.display.float_format = '{:.9f}'.format
df = pd.read_parquet(d, engine='pyarrow')
df.head
```

You will see over 6 million Line Item records.

For `parquet/tpch_orders/` directory do:

```python
os.system('ls -lA parquet/tpch_orders/')
d = 'parquet/tpch_orders/'
df = pd.read_parquet(d, engine='pyarrow')
df.head
```

