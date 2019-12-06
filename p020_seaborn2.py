import matplotlib.pyplot as plt
import seaborn as sns

fmri = sns.load_dataset("fmri")
sns.relplot(x="timepoint", y="signal", hue="event", kind="line", data=fmri);
plt.show()