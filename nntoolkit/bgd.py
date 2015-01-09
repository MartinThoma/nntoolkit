import numpy as np
import random
from sklearn.datasets.samples_generator import make_regression 
import pylab
from scipy import stats
from theano import tensor as T, function


def gradient_descent_2(alpha, x, y, numIterations):
    m = x.shape[0] # number of samples
    theta = np.array([[1,1]])


    T_x,T_y, T_z, T_theta, T_loss = T.dmatrices('x','y','z','theta','loss')
    find_hypothesis=function([T_x,T_theta],T.dot(T_x,T_theta))
    find_loss=function([T_x,T_y], T_x-T_y)
    find_cost=function([T_loss] ,  (T_loss**2 ).sum()/(2*m) )
    find_gradient=function([T_x,T_loss], (T.dot(T_x, T_loss)/m   ) )
    

#    theta=theta.reshape(theta.shape[0],1)
    for iter in range(0, numIterations):
        hypothesis =find_hypothesis(x, theta).T #TODO: could not emplement it without reshape
        loss=find_loss(hypothesis, np.array([y]))
        J = find_cost(loss)
        print "iter %s | J: %.3f" % (iter, J)   
        gradient = find_gradient(loss,x)
        find_theta=function([T_z,T_theta], T_theta - alpha*T_z )
        theta = find_theta(gradient.T,theta) #theta - alpha * gradient  # update
    return theta

if __name__ == '__main__':
    x, y = make_regression(n_samples=10, n_features=1, n_informative=1, 
                        random_state=0, noise=0) 
    #x 100x1
    #print type(y)

    print x.shape==y.shape
    #y 100x1
    m, n = np.shape(x)
    x = np.c_[ np.ones(m), x] # insert column
    alpha = 0.01 # learning rate
    theta = gradient_descent_2(alpha, x, y, 2000)

    print theta

    # plot
    for i in range(x.shape[1]):
        y_predict = theta[0] + theta[1]*x 
    pylab.plot(x[:,1],y,'o')
    pylab.plot(x,y_predict,'k-')
    pylab.show()
    print "Done!"