"""
Milestone 1 – Phase 1: Perception Module (Capsule Network)
This module implements a basic Capsule Network for 28×28 grayscale images (e.g. MNIST).
It demonstrates the dynamic routing algorithm for capsules and can be extended to
more complex sensory data in future milestones.

Classes:
    PrimaryCaps: Convolutional layer that produces primary capsules.
    DigitCaps: Capsule layer with dynamic routing, producing class capsules.
    CapsNet: End-to-end capsule network combining the above layers.

Functions:
    margin_loss: Loss function for training capsule networks.

Usage:
    python capsnet_m1.py  # trains the network on MNIST for a few epochs and prints accuracy.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class PrimaryCaps(nn.Module):
    """Primary capsule layer implemented as a convolution followed by a squash."""

    def __init__(self, in_channels: int = 256, caps_dim: int = 8, n_caps: int = 32,
                 kernel_size: int = 9, stride: int = 2) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, n_caps * caps_dim, kernel_size, stride)
        self.caps_dim = caps_dim
        self.n_caps = n_caps

    @staticmethod
    def squash(s: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        """Non-linear activation that scales vectors to have length between 0 and 1."""
        norm = torch.sqrt((s ** 2).sum(dim=-1, keepdim=True) + eps)
        scale = (norm ** 2) / (1.0 + norm ** 2)
        return scale * (s / (norm + eps))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [batch, in_channels, H, W] -> [batch, n_caps*H*W, caps_dim]
        u = self.conv(x)
        B, C, H, W = u.size()
        u = u.view(B, self.n_caps, self.caps_dim, H, W).permute(0, 3, 4, 1, 2).contiguous()
        u = u.view(B, -1, self.caps_dim)
        return self.squash(u)


class DigitCaps(nn.Module):
    """Digit capsule layer with dynamic routing."""

    def __init__(self, n_in_caps: int, in_dim: int, n_classes: int = 10,
                 out_dim: int = 16, routing_iters: int = 3) -> None:
        super().__init__()
        self.n_in_caps = n_in_caps
        self.n_classes = n_classes
        self.routing_iters = routing_iters
        # Transformation matrix for each pair of input and output capsules
        self.W = nn.Parameter(0.01 * torch.randn(1, n_in_caps, n_classes, out_dim, in_dim))

    @staticmethod
    def squash(s: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        norm = torch.sqrt((s ** 2).sum(dim=-1, keepdim=True) + eps)
        scale = (norm ** 2) / (1.0 + norm ** 2)
        return scale * (s / (norm + eps))

    def forward(self, u: torch.Tensor) -> torch.Tensor:
        # u: [batch, N_in, in_dim]
        B, N, D = u.size()
        # Expand transformation matrix to batch dimension
        W = self.W.repeat(B, 1, 1, 1, 1)
        # Predict output capsule vectors: [B,N,C,out_dim]
        u_hat = torch.matmul(W, u.unsqueeze(2).unsqueeze(-1)).squeeze(-1)
        b = torch.zeros(B, N, self.n_classes, 1, device=u.device)
        for _ in range(self.routing_iters):
            c = F.softmax(b, dim=2)
            s = (c * u_hat).sum(dim=1, keepdim=True)
            v = self.squash(s)
            if _ < self.routing_iters - 1:
                agreement = (u_hat * v).sum(dim=-1, keepdim=True)
                b = b + agreement
        return v.squeeze(1)  # [batch, C, out_dim]


class CapsNet(nn.Module):
    """End-to-end Capsule Network for 28×28 grayscale inputs."""

    def __init__(self, n_classes: int = 10) -> None:
        super().__init__()
        # Initial conv layer
        self.stem = nn.Sequential(
            nn.Conv2d(1, 256, kernel_size=9, stride=1), nn.ReLU(inplace=True)
        )
        # Primary capsules: reduces spatial dims and increases channels
        self.primary = PrimaryCaps(in_channels=256, caps_dim=8, n_caps=32, kernel_size=9, stride=2)
        # Calculate number of capsules after primary layer (approx 6×6 for 28×28 input)
        self.n_in_caps = 32 * 6 * 6
        self.digits = DigitCaps(n_in_caps=self.n_in_caps, in_dim=8,
                               n_classes=n_classes, out_dim=16)

    def forward(self, x: torch.Tensor) -> tuple:
        x = self.stem(x)
        u = self.primary(x)
        v = self.digits(u)
        logits = v.norm(dim=-1)
        return logits, v


def margin_loss(logits: torch.Tensor, target: torch.Tensor, m_pos: float = 0.9,
                m_neg: float = 0.1, lambda_: float = 0.5) -> torch.Tensor:
    """Margin loss used in capsule networks.

    Args:
        logits: Predicted capsule lengths [batch, num_classes].
        target: Ground truth labels [batch].
        m_pos: Positive margin threshold.
        m_neg: Negative margin threshold.
        lambda_: Down-weighting factor for absent classes.

    Returns:
        Tensor containing the mean margin loss.
    """
    B, C = logits.shape
    y = F.one_hot(target, C).float()
    L_pos = F.relu(m_pos - logits).pow(2)
    L_neg = F.relu(logits - m_neg).pow(2)
    L = y * L_pos + lambda_ * (1 - y) * L_neg
    return L.sum(dim=1).mean()


def train_capsnet(epochs: int = 5, batch_size: int = 128, lr: float = 1e-3) -> None:
    """Simple training loop for CapsNet on MNIST."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = CapsNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    transform = transforms.Compose([transforms.ToTensor()])
    train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    test_set = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_set, batch_size=256, shuffle=False, num_workers=4)

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            logits, _ = model(x)
            loss = margin_loss(logits, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * x.size(0)
        avg_loss = total_loss / len(train_loader.dataset)
        # Evaluate accuracy on test set
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for x, y in test_loader:
                x, y = x.to(device), y.to(device)
                logits, _ = model(x)
                preds = logits.argmax(dim=1)
                correct += (preds == y).sum().item()
                total += y.size(0)
        acc = correct / total
        print(f"Epoch {epoch+1}: loss={avg_loss:.4f}, accuracy={acc:.4f}")


if __name__ == '__main__':
    train_capsnet()