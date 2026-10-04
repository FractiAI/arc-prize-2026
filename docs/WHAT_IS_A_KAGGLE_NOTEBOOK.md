# What is a Kaggle Notebook? (plain language)

You do **not** need to become a Kaggle expert.

A **Kaggle Notebook** (also called a **Kernel**) is simply:

> A page on kaggle.com that runs our Python file on Kaggle’s computers, with the competition files already attached.

That’s it. Same idea as opening a Google Doc that can also press “Run.”

## Why we use one

ARC-AGI-2 is a **Code Competition**. Kaggle wants the answer file (`submission.json`) to be **produced by a run on their site**, not only uploaded from a laptop. Direct CLI upload returned **403 Forbidden** for us.

## What I already did for you

I pushed and ran our solver as a private script kernel:

**https://www.kaggle.com/code/prudenciomendez/fractiai-arc-agi-2-dsl-v1**

It finished successfully and wrote `submission.json` (240 tasks).

## What you may still need to click (30 seconds)

If the API cannot “Submit to Competition” (we still see 403), open that link while logged into Kaggle as **prudenciomendez**, then:

1. Open the latest **Version** that shows a green check / Complete  
2. Look for **Submit to Competition** (or **Submit**)  
3. Confirm the message (e.g. `FractiAI DSL v1`)

After that, scores appear under the competition’s **Submissions** tab:

https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/submissions

## AGI-3 is different

ARC-AGI-3 uses an **ARC API key** from https://three.arcprize.org/ (not the Kaggle token). Paste `ARC_API_KEY=...` in chat or add it as a Cloud Agent secret so this machine can run the agent kit.
