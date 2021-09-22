from tools import *

cmap = mpl.colors.ListedColormap(['black', 'green','blue','red'])
bounds=[-0.5,0.5,1.5,2.5,3.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


N = 200
vac = 0.6
t = 1000
dead = 15
prob_d = 0.05
tab_X = np.zeros(((t, N, N)))

tab_X[0] = Disease(N, dead, prob_d).initial(vac = vac)
tab_X[0] = Disease(N, dead, prob_d).place_first(tab_X[0])

count = np.zeros(tab_X[0].shape)

print("\n Computing...\n \n")

for i in tqdm(range(t-1)):
    #print(i)
    tab_X[i+1] = Disease(N, dead, prob_d).update_loop(tab_X[i], 0.2)
    count = Disease(N, dead, prob_d).count(count, tab_X[i+1])
    tab_X[i+1], count = Disease(N, dead, prob_d).transform_dead(count, tab_X[i+1])

tab_d, tab_i, tab_h = Disease(N, dead, prob_d).counting(tab_X, t)

fig, (ax1) = plt.subplots(ncols=1)
im=ax1.imshow(tab_X[0], cmap=cmap, norm=norm)

def animate(n):
    im.set_data(tab_X[n])
    return im,

inter = 3
ani = animation.FuncAnimation(fig, animate, frames=range(tab_X.shape[0]), blit=True, interval=inter, repeat=True)
plt.show()

plt.figure()
plt.plot(tab_d, '-k', label = 'Dead')
plt.plot(tab_i, '-r', label = 'Infected')
plt.plot(tab_h, '-g', label = 'Healty')
plt.title("Probability to die : {:.2f} \n Percentage of vaccinated : {:.0f}".format(prob_d, vac*100))
plt.legend()
plt.savefig('Disease_sim_{}_prob_d_{}.png'.format(N**2, prob_d))
plt.show()

writergif = animation.PillowWriter(fps=25)
ani.save('Disease_sim_{}_prob_d_{}.gif'.format(N**2, prob_d),writer=writergif)
