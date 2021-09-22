from tools import *

cmap = mpl.colors.ListedColormap(['black', 'green','blue','red'])
bounds=[-0.5,0.5,1.5,2.5,3.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


N = 200
vac = np.arange(0, 1, 0.1)
t = 1000
dead = 15
prob_d = 0.05
tab_X = np.zeros((((len(vac), t, N, N))))
tab_i_v = np.zeros((len(vac), t))

for indv, v in enumerate(vac):

    print("\n \n % of vaccinated = {:.0f} \n \n".format(v*100))

    tab_X[indv, 0] = Disease(N, dead, prob_d).initial(vac = v)
    tab_X[indv, 0] = Disease(N, dead, prob_d).place_first(tab_X[indv, 0])

    count = np.zeros(tab_X[0, 0].shape)

    for i in tqdm(range(t-1)):
        #print(i)
        tab_X[indv, i+1] = Disease(N, dead, prob_d).update_loop(tab_X[indv, i], 0.2)
        count = Disease(N, dead, prob_d).count(count, tab_X[indv, i+1])
        tab_X[indv, i+1], count = Disease(N, dead, prob_d).transform_dead(count, tab_X[indv, i+1])

    tab_d, tab_i, tab_h = Disease(N, dead, prob_d).counting(tab_X[indv], t)

    tab_i_v[indv] = tab_i

plt.figure()
for k in range(len(vac)):
    plt.plot(tab_i_v[k], label = '{:.0f} %'.format(vac[k]*100))
plt.title("Number of infected as function of % of vaccinated")
plt.legend()
plt.savefig('Varying_vac_{}.png'.format(N**2))
plt.show()
