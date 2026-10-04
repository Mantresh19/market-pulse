import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing(as_frame=True)
df = housing.frame

print("Data shape (rows, columns):", df.shape)
df.head()

print("Summary Statistics")
print(df.describe().T[['mean', 'std', 'min', '50%', 'max']])

plt.figure(figsize = (7,4))
sns.histplot(df['MedHouseVal'], kde = True, bins=40, color='royalblue')
plt.title('Target Distribution: Median House Value ($100,000s)')
glt.clabel('MedHouseVal')
plt.ylabel('Count')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()