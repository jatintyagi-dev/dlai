# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_mbtraining.ipynb.

# %% auto 0
__all__ = ['loss_func', 'dataset', 'DL', 'report', 'opt', 'fit']

# %% ../nbs/02_mbtraining.ipynb 1
import pickle,gzip,math,os,time,shutil,torch,matplotlib as mpl,numpy as np,matplotlib.pyplot as plt
from pathlib import Path
from torch import tensor,nn
import torch.nn.functional as F
import fastcore.all as fc
from functools import partial
from fastcore.test import test_close

# %% ../nbs/02_mbtraining.ipynb 10
class dataset():
    def __init__(self, x, y):fc.store_attr()
        
    def __getitem__(self,i):
        return self.x[i],self.y[i]
    def __len__(self):
        return len(self.x)

# %% ../nbs/02_mbtraining.ipynb 13
class DL:
    def __init__(self, ds, bs):fc.store_attr()
        
#     def __call__(self):
#         for i in range(0,len(self.x),self.bs):
#             yield self.x[i:i+bs], self.y[i:i+bs]
    def __iter__(self):
        for i in range(0,len(self.ds),self.bs):
            yield self.ds[i:i+self.bs]
    
#     def __repr__(self):
#         return f"shape of x{self.ds[0].shape} \n, shape of y{self.ds[1].shape} {self.bs} "
        
        
        

# %% ../nbs/02_mbtraining.ipynb 19
loss_func = F.cross_entropy

# %% ../nbs/02_mbtraining.ipynb 22
def report(loss, preds, yb,train="training"): print(f' {train} Loss: {loss:.2f}, Accuracy: {accuracy(preds, yb):.2f}')

# %% ../nbs/02_mbtraining.ipynb 31
class opt():
    def __init__(self, params , lr=0.5):self.params,self.lr=list(params),lr
    
    def zero_grad(self):
        for p in self.params: p.grad.data.zero_() 
        
        
    
    def step(self):
        with torch.no_grad():
            for p in self.params:
                p -= self.lr * p.grad
    

# %% ../nbs/02_mbtraining.ipynb 33
def fit(model, epochs=3, lr = 0.2):
    
    o = opt(model.parameters())
#     o= Optimizer(model.parameters())
    for epoch in range(epochs):
        model.train()
        for xb, yb in train_dl:
            preds = model(xb)
    #         print(preds.squeeze(dim=1).shape)
    #         print(yb.shape)
            loss = loss_func(preds, yb)
            
            loss.backward()
            o.step()
            o.zero_grad()
    
        report(loss, preds, yb, "training ")
    
        model.eval()    
        with torch.no_grad():
            for xb, yb in valid_dl:
                preds = model(xb)
                loss = loss_func(preds, yb)
                
#         print(preds.shape)
        report(loss, preds, yb, "validation ")
            
        

# %% ../nbs/02_mbtraining.ipynb 38
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler, BatchSampler
