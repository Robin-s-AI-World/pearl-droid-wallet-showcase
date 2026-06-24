<!--
Status: Draft v1 — feature piece for the showcase.
Purpose: search-target + honest segue to the wallet. Tone: sardonic-rigorous, no marketing scent.
Coinages (author's): "dysworkful"; "proof-of-potentially-saleable-hopefully-useful-maths-puzzles".
-->

# Proof of Useful Work? What "useful" is actually buying you.

A miner, somewhere, pulls up the workload his rig has been grinding for the last six hours — the "useful AI compute" his GPU is allegedly performing to secure the Pearl chain — and goes looking for the AI. He expects to find, somewhere in there, the ghost of a conversation: a token, a prompt fragment, the faint smell of GPT. He finds dense, opaque slabs of matrix multiplication and nothing that decodes back to a word. Conclusion, posted to a forum: *it's a scam, the "useful work" is fake.*

Which is the moment to lean in, in our most sincere con-man cadence, and offer him a beautiful matmul, just below sea level, in the Netherlands.

He's wrong. He's also right. And the fact that he can be both at once is the entire problem with the word "useful" in *Proof-of-Useful-Work*.

***

He's wrong about the test. Large language model inference is, in bulk, matrix multiplication. The attention heads and the feed-forward layers are matmuls against weight matrices, and at the GPU what you see is wave after wave of multiply-accumulate on float tensors — no words, no prompts, no conversation. A conversation is not a feature of the compute; it's an emergent decode that requires the exact weights, the tokenizer, and the routing, none of which the miner has, and none of which he should. The absence of legible chat in his workload is *precisely* what genuine LLM matmul looks like. He went searching for the smell of intelligence and concluded, from the absence of smell, that nothing was cooking. The kitchen doesn't smell like the meal.

But his instinct is correct, and sharper than his test. From the compute layer — from his seat — he cannot tell genuine, externally-demanded matmul apart from a contrived matmul puzzle that is mathematically identical in shape but backed by no model and no buyer. Both look like the same opaque slabs. The property he's trying to verify — *did someone actually request and pay for this compute?* — is a property of the demand side, and the demand side is, by construction, invisible to the person performing the work. The miner is structurally the worst-situated person on earth to confirm usefulness: he is staring at the supply and demanding to see the demand, which is not there to be seen whether it exists or not.

***

And that is the whole trouble with "useful." In Proof-of-Useful-Work, *useful* is not a property the worker can observe; it is a claim the protocol asserts. Strip the marketing, and what the miner can actually verify from his seat is: *I performed a large volume of non-arbitrary matrix multiplication.* Whether that matmul served a real external customer, or was a matmul-shaped lottery dressed for the occasion, is — from the seat — indistinguishable. Hence, charitably, the grade we give it: not useful, but **dysworkful** — work shaped like useful work, work that may even *be* useful work, whose usefulness is asserted rather than evident.

The honest move is to stop letting "useful" do unearned work and split the question along two axes:

1. **Is the work non-arbitrary** — real computation, not an adversarial hash lottery?
2. **Is there external demand** — would someone pay for this compute if no coin existed?

| Scheme | Non-arbitrary? | Externally demanded? | Honest verdict |
|---|---|---|---|
| Bitcoin | No (adversarial hashes) | No — and proudly | Honest: a lottery that calls itself a lottery |
| Primecoin | Yes (Cunningham prime chains) | No — real maths, zero buyers | *Proof-of-non-arbitrary-work*, not useful |
| Filecoin (PoRep / PoSt) | Yes (prove you stored X) | Conditional — only if the data is *wanted* | *Proof-of-storage*, useful on a contingency |
| Folding / @home-style | Yes | Yes — someone funds the science | *The* clean case: genuinely useful |
| Pearl (matrix-mul AI inference) | Yes | **Arguably** — real compute-market demand… | …and this is where "dysworkful" earns its keep |

Reserve the word *useful* for schemes that clear **both** axes. Everything else gets an honest name: proof-of-non-arbitrary-work, proof-of-storage, proof-of-replication — or, for the aspirational middle where the demand is hoped-for rather than demonstrated, **proof-of-potentially-saleable-hopefully-useful-maths-puzzles**.

***

Where does Pearl land? Axis one, cleanly: it is real matmul, not a hash. That is not nothing — most schemes wearing the "useful" label don't clear even that bar honestly. Axis two is the live question, and it is exactly the question our forum miner could not answer from his seat: is the AI-compute demand *genuine* (a buyer who'd pay fiat for that inference regardless of the token), or *circular* (token issuance subsidizing compute that is only "purchased" in order to mine the token)? Pearl has a better story here than most — the compute-market demand rooted in outfits like Together and the vast.ai marketplace is a real thing that exists outside the coin — but "a better story" and "verifiable from the seat" are different sentences, and the honest version of the second is: *not from the seat you are sitting in.*

So: not a scam — the matmul is real, and the demand is at least plausible and externally rooted. And not obviously-useful — the demand is asserted, not observable at the point of work. The defensible position is the uncomfortable middle: the work is genuine computation whose usefulness you are asked to take on attestation. A mature ecosystem says that out loud instead of pretending the question does not exist — which is, not coincidentally, the only posture from which you can build a tool for the chain without lying to the people who'd use it.

***

Which is the only honest way to introduce a wallet built for this chain. We do not require you to land on "useful" or "dysworkful." We do not ask you to believe. We ask a smaller, cleaner question: whatever PRL turns out to be — the Bitcoin of AI compute, a matmul coin with asserted usefulness, or something that settles somewhere in between — do you want sole custody of the coins you hold, the ability to move them on your own authority, and a live read on what they are trading for, without entrusting any of that to a desktop app you have to boot up, an exchange you have to trust, or an organization you have to believe in? If yes, the wallet is for you. And the way it is built — a release-signed APK you verify by hash, no Play-Store organization games, your recovery phrase imported by camera and wiped from the image on the spot so it is never stored as a photograph — is the same honesty applied to the product that this paper has tried to apply to the category.

The matmul below sea level is real. You just cannot see it from the dock. That is not a scandal; it is a property of the layer you happen to be standing on. The scandal would be selling you the word *useful* without admitting that.
