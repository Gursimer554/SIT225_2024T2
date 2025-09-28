import pandas as pd, matplotlib.pyplot as plt
df = pd.read_csv("occupancy_log.csv")
df['t']=(df['time_ms']-df['time_ms'].iloc[0])/1000

# timelines
plt.figure(); plt.step(df['t'], df['PIR'], where='post', label='PIR')
plt.step(df['t'], df['presence'], where='post', label='Fusion presence')
plt.xlabel('Time (s)'); plt.ylabel('State'); plt.legend(); plt.tight_layout()
plt.savefig('presence_timeline.png', dpi=200)

plt.figure(); plt.plot(df['t'], df['distance_cm'])
plt.xlabel('Time (s)'); plt.ylabel('Distance (cm)'); plt.tight_layout()
plt.savefig('distance_timeline.png', dpi=200)

# simple PIR-only false alarms: PIR==1 while fusion says 0
pir_only_false = ((df['PIR']==1) & (df['presence']==0)).sum()
fusion_false   = 0  # under rule v1
plt.figure(); plt.bar(['PIR-only','Fusion'], [pir_only_false, fusion_false])
plt.ylabel('False alarms'); plt.tight_layout()
plt.savefig('false_alarms.png', dpi=200)
