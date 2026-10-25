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
    def __init__(self,length=24,width=128,flow=True,residual=False):
        super().__init__()
        self.length=length; self.flow=flow; self.residual=residual
        dim=5*length+7 if flow else 4*length+3
        self.net=nn.Sequential(nn.Linear(dim,width),nn.SiLU(),ResidualBlock(width),
                               ResidualBlock(width),nn.LayerNorm(width),nn.Linear(width,length))

    def forward(self,source,condition,z=None,tau=None):
        inputs=[source,condition]
        if self.flow:
            inputs += [z,tau,torch.sin(torch.pi*tau),torch.cos(torch.pi*tau),tau*tau]
        output=self.net(torch.cat(inputs,dim=-1))
        return source+output if self.residual and not self.flow else output


def integrate(model,source,condition,steps=4):
    """Differentiable explicit midpoint solver in flow time tau in [0,1]."""
    z=source
    h=1./steps
    for j in range(steps):
        tau=torch.full((len(z),1),j*h,device=z.device,dtype=z.dtype)
        f=model(source,condition,z,tau)
        z=z+h*model(source,condition,z+h*f/2,tau+h/2)
    return z


def single_step(model,source,condition):
    """One Euler step: evaluate velocity at tau=0, reach tau=1 in one call."""
    tau=source.new_zeros((len(source),1))
    return source+model(source,condition,source,tau)


def predict_window(model,source,condition,steps=4,predictor='midpoint'):
    if not model.flow:
        return model(source,condition)
    if predictor=='single_step':
        return single_step(model,source,condition)
    if predictor=='midpoint':
        return integrate(model,source,condition,steps)
    raise ValueError(f'Unknown predictor: {predictor}')


def flow_loss(model,source,target,condition,endpoint_weight=1.,steps=4,predictor='midpoint'):
    tau=torch.rand((len(source),1),device=source.device)
    z=(1-tau)*source+tau*target
    vf=model(source,condition,z,tau)
    loss_fm=(vf-(target-source)).square().mean()
    # Integrate from the actual source: endpoint supervision cannot read target.
    if endpoint_weight:
        pred=predict_window(model,source,condition,steps,predictor)
        loss_result=(pred-target).square().mean()+4*(pred[:,0]-target[:,0]).square().mean()
    else:
        loss_result=loss_fm.new_zeros(())
    return loss_fm+endpoint_weight*loss_result,loss_fm,loss_result
