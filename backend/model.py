import torch
import torch.nn as nn
import torchvision.models as models

class MyResNet18(nn.Module):
    def __init__(self, num_classes=10):
        super(MyResNet18, self).__init__()
        # Load a pretrained ResNet18
        self.resnet = models.resnet18(pretrained=True)
        
        # (Optional) Freeze pretrained layers if you only want to train the final layer
        # for param in self.resnet.parameters():
        #     param.requires_grad = False

        # Replace the final FC layer to match num_classes
        in_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(in_features, num_classes)

    def forward(self, x):
        return self.resnet(x)
