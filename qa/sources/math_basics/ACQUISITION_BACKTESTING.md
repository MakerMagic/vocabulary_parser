# Stage 1 Acquisition Backtesting: `math_basics`

To verify Stage 1 acquisition integrity:

```powershell
.\.venv\Scripts\python.exe -c "
from processors.provenance import sha256_file
from pathlib import Path
sha = sha256_file(Path('acquisition/sources/math_basics/math_basics.txt'))
assert sha == 'eb6ea47dabd2e54b17a514781edb9b577145d865d9928495cc40ab8cbf09e698'
print('Acquisition hash locked:', sha)
"
```
