import numpy as np
from modules.planar_utils import sigmoid


def layer_sizes(X, Y):
    
    n_x = X.shape[0]
    n_h = 4
    n_y = Y.shape[0]
    
    return (n_x, n_h, n_y)

def initialize_parameters(n_x, n_h, n_y):
    
    W1 = np.random.randn(n_h,n_x) * 0.01
    b1 = np.zeros((n_h,1))
    W2 = np.random.randn(n_y,n_h) * 0.01
    b2 = np.zeros((n_y,1))
    
    assert (W1.shape == (n_h, n_x))
    assert (b1.shape == (n_h, 1))
    assert (W2.shape == (n_y, n_h))
    assert (b2.shape == (n_y, 1))
    
    parameters = {"W1": W1,
                "b1": b1,
                "W2": W2,
                "b2": b2}
    
    return parameters

def forward_propagation(X, parameters):
    
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    
    Z1 = np.dot(W1,X) + b1
    A1 = np.tanh(Z1)
    
    Z2 = np.dot(W2,A1) + b2
    A2 = sigmoid(Z2)
    
    assert(A2.shape == (1, X.shape[1]))
    
    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}
    
    return A2, cache

def compute_cost(A2, Y, parameters):
    
    m = Y.shape[1]
    logprobs = np.dot(Y,np.log(A2).T) + np.dot((1 - Y),np.log(1 - A2).T)
    cost = np.float64(-logprobs / m)
    cost = np.squeeze(cost)
    assert(isinstance(cost, float))
    
    return cost

def backward_propagation(parameters, cache, X, Y):

    m = Y.shape[1]
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    Z1 = cache["Z1"]
    A1 = cache["A1"]
    Z2 = cache["Z2"]
    A2 = cache["A2"]

    dZ2 = A2 - Y
    dW2 = (np.dot(dZ2,A1.T))/m
    db2 = (np.sum(dZ2, axis = 1, keepdims = True))/m
    dtanh = 1 - np.power(A1,2)
    dZ1 = np.dot(W2.T,dZ2) * dtanh
    dW1 = (np.dot(dZ1,X.T))/m
    db1 = (np.sum(dZ1, axis = 1, keepdims = True))/m

    grads = {"dW1": dW1,
        "db1": db1,
        "dW2": dW2,
        "db2": db2}

    return grads

def update_parameters(parameters, grads, learning_rate = 1.2):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]
    
    W1 = W1 - (learning_rate * dW1)
    b1 = b1 - (learning_rate * db1)
    W2 = W2 - (learning_rate * dW2)
    b2 = b2 - (learning_rate * db2)

    parameters = {"W1": W1,
                "b1": b1,
                "W2": W2,
                "b2": b2}
    
    return parameters

def nn_model(X, Y, n_h, num_iterations = 10000, print_cost=False):

    n_x, n_h, n_y = layer_sizes(X, Y)
    parameters = initialize_parameters(n_x, n_h, n_y)
    
    
    for i in range(0, num_iterations):
        
        A2,cache = forward_propagation(X, parameters)
        
        cost = compute_cost(A2, Y, parameters)
        if print_cost and i % 1000 == 0: print ("Cost after iteration %i: %f" %(i, cost))
        
        grads = backward_propagation(parameters, cache, X, Y)
        
        parameters = update_parameters(parameters, grads)
        
    return parameters

def predict(parameters, X):
    
    A2, cache = forward_propagation(X, parameters)
    predictions = (A2 > .5)
    
    return predictions