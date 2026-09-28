"""
A tiny GPT: the same Transformer idea as Episode 1, in about 80 lines.
迷你 GPT：和第 1 集一样的 Transformer，大约 80 行代码。

It works one character at a time: given the characters so far, predict the next one.
它一个字一个字地工作：看到前面的字，预测下一个字。
Used by 3_train_poet.py (training) and 4_write_poems.py (writing).
"""
import torch
from torch import nn
from torch.nn import functional as F


class SelfAttention(nn.Module):
    """Every character looks back at the earlier characters and decides which ones matter (Episode 1).
    每个字回头看前面的字，决定哪些字重要（第 1 集）。"""

    def __init__(self, n_embd, n_head, dropout):
        super().__init__()
        self.n_head, self.dropout = n_head, dropout
        self.qkv = nn.Linear(n_embd, 3 * n_embd)   # makes a Query, Key and Value for every character / 为每个字算出 Q、K、V
        self.proj = nn.Linear(n_embd, n_embd)

    def forward(self, x):
        B, T, E = x.shape                          # batch size, number of characters, vector size / 批大小、字数、向量长度
        q, k, v = self.qkv(x).split(E, dim=2)
        # split each vector into several "heads" that each pay attention to different things
        # 把向量分成几个“头”，每个头关注不同的东西
        q, k, v = (t.view(B, T, self.n_head, E // self.n_head).transpose(1, 2) for t in (q, k, v))
        # softmax(Q·K / √d) · V  -- with a mask so no character can peek at the future (is_causal=True)
        # softmax(Q·K / √d) · V —— 加上遮罩，不许偷看后面的字（is_causal=True）
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True, dropout_p=self.dropout if self.training else 0)
        return self.proj(y.transpose(1, 2).reshape(B, T, E))


class Block(nn.Module):
    """One Transformer layer: attention, then a small feed-forward network. / 一层 Transformer：注意力 + 前馈网络。"""

    def __init__(self, n_embd, n_head, dropout):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(n_embd), nn.LayerNorm(n_embd)
        self.attn = SelfAttention(n_embd, n_head, dropout)
        self.mlp = nn.Sequential(nn.Linear(n_embd, 4 * n_embd), nn.GELU(), nn.Linear(4 * n_embd, n_embd), nn.Dropout(dropout))

    def forward(self, x):
        x = x + self.attn(self.ln1(x))   # "+ x" keeps the original information flowing (a residual connection) / 残差连接
        x = x + self.mlp(self.ln2(x))
        return x


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, block_size=128, n_embd=384, n_head=6, n_layer=6, dropout=0.1):
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, n_embd)     # each character -> a vector (Episode 13) / 每个字 → 一个向量
        self.pos_emb = nn.Embedding(block_size, n_embd)     # where it is in the text / 它在第几个位置
        self.blocks = nn.Sequential(*[Block(n_embd, n_head, dropout) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.head = nn.Linear(n_embd, vocab_size)           # a score for every possible next character / 给每个可能的下一个字打分

    def forward(self, idx, targets=None):
        T = idx.shape[1]
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        logits = self.head(self.ln_f(self.blocks(x)))
        loss = None
        if targets is not None:   # how surprised were we by the real next characters? (Episode 13) / 对真正的下一个字有多“意外”？
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new, temperature=0.8, stop=None, force=None):
        """Write max_new more characters. / 再写 max_new 个字。
        temperature: lower = safer, higher = wilder (Episode 3). / 温度：低 = 保守，高 = 大胆（第 3 集）。
        stop: a character id that means "the end". / 遇到这个字就停。
        force: a function(idx) -> character id or None, used for acrostic poems. / 用来写藏头诗。"""
        self.eval()
        for _ in range(max_new):
            nxt = force(idx) if force else None
            if nxt is None:
                logits, _ = self(idx[:, -self.block_size:])
                probs = F.softmax(logits[:, -1, :] / temperature, dim=-1)   # scores -> probabilities / 分数 → 概率
                nxt = torch.multinomial(probs, num_samples=1).item()        # roll the dice / 按概率掷骰子
            idx = torch.cat([idx, torch.tensor([[nxt]], device=idx.device)], dim=1)
            if stop is not None and nxt == stop:
                break
        return idx
