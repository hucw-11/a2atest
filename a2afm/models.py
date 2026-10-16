import torch
from torch import nn


class ResidualBlock(nn.Module):
    def __init__(self,width):
        super().__init__()
        self.net=nn.Sequential(nn.LayerNorm(width),nn.Linear(width,width),nn.SiLU(),nn.Linear(width,width))
    def forward(self,x):
        return x+self.net(x)*.5


class WindowNet(nn.Module):
    """Dense temporal residual network. Flow state stays in R^L, no latent AE."""
    def __init__(self,length=24,width=128,flow=True):
        super().__init__()
        self.length=length; self.flow=flow
        dim=5*length+7 if flow else 4*length+3
        self.net=nn.Sequential(nn.Linear(dim,width),nn.SiLU(),ResidualBlock(width),
                               ResidualBlock(width),nn.LayerNorm(width),nn.Linear(width,length))

    def forward(self,source,condition,z=None,tau=None):
        inputs=[source,condition]
        if self.flow:
            inputs += [z,tau,torch.sin(torch.pi*tau),torch.cos(torch.pi*tau),tau*tau]
        return self.net(torch.cat(inputs,dim=-1))


def integrate(model,source,condition,steps=4):
    """Differentiable explicit midpoint solver in flow time tau in [0,1]."""
    z=source
    h=1./steps
    for j in range(steps):
        tau=torch.full((len(z),1),j*h,device=z.device,dtype=z.dtype)
        f=model(source,condition,z,tau)
        z=z+h*model(source,condition,z+h*f/2,tau+h/2)
    return z


def flow_loss(model,source,target,condition,endpoint_weight=1.,steps=4):
    tau=torch.rand((len(source),1),device=source.device)
    z=(1-tau)*source+tau*target
    vf=model(source,condition,z,tau)
    loss_fm=(vf-(target-source)).square().mean()
    # Integrate from the actual source: endpoint supervision cannot read target.
    if endpoint_weight:
        pred=integrate(model,source,condition,steps)
        loss_result=(pred-target).square().mean()+4*(pred[:,0]-target[:,0]).square().mean()
    else:
        loss_result=loss_fm.new_zeros(())
    return loss_fm+endpoint_weight*loss_result,loss_fm,loss_result
