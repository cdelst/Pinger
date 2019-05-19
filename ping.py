import  matplotlib.pyplot     as         plt 
import  matplotlib.animation  as         animation 
import  matplotlib.patches    as         mpatches
from    matplotlib            import     style 
from    pythonping            import     ping
from    datetime              import     datetime 
import  pandas                as         pd 
import  os 







style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
df = pd.DataFrame(columns=['Time', 'Min', 'Avg', 'Max'])

def animate(i):
    global df
    
    #Format is min/avg/max, first breaks lines picks 6th, then breaks words picks 6th, then splits format into 3 nums
    pingStats = str(ping('8.8.8.8')).split('\n')[5].split(' ')[5].split('/')

    #Format to floats
    for i in range(len(pingStats)):
        pingStats[i] = float(pingStats[i])

    #Add to already existing data frame
    dfAppend = df.append({'Time' : str(datetime.now()).split(' ')[1][0 : -7], 
                        'Min' : pingStats[0], 
                        'Avg' : pingStats[1], 
                        'Max' : pingStats[2]}, 
                        ignore_index=True)

    targetXTicks = 50
    while dfAppend.shape[0] > targetXTicks:
        dfAppend = dfAppend.drop([0])
   
    print(dfAppend)
    df = dfAppend
    print()

    xs = []
    ys = []

    ax1.clear()
    ax1.plot(df['Time'], df['Min'], label='Min', linewidth=2, color='green')
    ax1.plot(df['Time'], df['Avg'], label='Avg', linewidth=2, color='orange')
    ax1.plot(df['Time'], df['Max'], label='Max', linewidth=2, color='red')
    
    ax1.set_ylim([-10, 100])
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Ping (in ms)')
    plt.title('Ping')

    minPatch = mpatches.Patch(color='green', label='Min')
    avgPatch = mpatches.Patch(color='orange', label='Avg')
    maxPatch = mpatches.Patch(color='red', label='Max')
    plt.legend(handles=[minPatch, avgPatch, maxPatch])


    every_nth = 11
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)


ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
plt.show()
