# Lybic SDK (Python)

Lybic (/ˈlaɪbik/) is a GUI agent infra service, provides ready-to-use GUI boxes for agent developers.

While building GUI agent, you may need to run a GUI box for your agent tasks, isolated and hosted on the cloud, without setting up instances and images yourself.

With Lybic SDK, you can easily create as many boxes as you want at any time, and control them without writing any automation code. Meanwhile, you and your users can easily access the desktop stream of the box, watching what your agent is doing, and interact with the box to fit "human-in-the-loop" scenarios.


## Install
```bash
pip install lybic
```

## Use

```python
from lybic import LybicClient

cli = LybicClient(
    org_id="xxx",
    api_key="xxx"
)
```

