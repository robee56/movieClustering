def primes(int kmax):
    cdef int n, k, i
    cdef int p[1000]
    result = []
    if kmax > 1000:
        kmax = 1000
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i = i + 1
        if i == k:
            p[k] = n
            k = k + 1
            result.append(n)
        n = n + 1
    return result


def objectiveFunction(self,,individu,k):
    #La fonction objective est une fonction qui a pour but de calculer la distance des centroides
    #des donnes, la somme de ces distances permet de savoir que le minimum est le meilleur ensemble de centroides
    m = shape(self.data)[0]
    clusterAssment = mat(zeros((m,2)))
    individu = np.array(individu)
    # print individu
    for i in range(m):
        minDist = inf; minIndex = -1
        for j in range(k):
            distJI = self.distEuclid(individu[j,:],self.data[i,:])
            if distJI < minDist:
                minDist = distJI; minIndex = j
        if clusterAssment[i,0] != minIndex: clusterChanged = True
        clusterAssment[i,:] = minIndex,minDist**2

    for cent in range(k):
        ptsInClust = self.data[nonzero(clusterAssment[:,0].A==cent)[0]]
        individu[cent,:] = mean(ptsInClust, axis=0)

    return individu,np.sum(clusterAssment[:,1])