# TPC-H Test data for IBIS, PyArrow e Pandas using Parquet

Example:

```python
import pyarrow as pa
d = 'parquet/tpch_lineitem/'
pd.options.display.float_format = '{:.9f}'.format
df = pd.read_parquet(d, engine='pyarrow')
df.head
```

You will see over 6 million Line Item records.

