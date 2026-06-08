from pathlib import Path
from typing import ClassVar

from pier.agents.installed.mini_swe_agent import MiniSweAgent
from pier.environments.base import BaseEnvironment
from pier.models.agent.name import AgentName


_CONTAINER_PKG_PATH = "/tmp/mini-swe-agent-deepmorph-src"
_DEFAULT_LOCAL_PATH = Path(__file__).parents[4] / "mini-swe-agent-deepmorph"


class MiniSweAgentDeepmorphh(MiniSweAgent):
    """
    Variant of MiniSweAgent that installs mini-swe-agent-deepmorph from a local source tree.
    """

    _AGENT_PACKAGE: ClassVar[str] = "mini-swe-agent-deepmorph"
    _AGENT_EXECUTABLE: ClassVar[str] = "mini-swe-agent-deepmorph"

    def __init__(self, *args, local_package_path: Path | str = _DEFAULT_LOCAL_PATH, **kwargs):
        super().__init__(*args, **kwargs)
        self._local_package_path = Path(local_package_path)

    @staticmethod
    def name() -> str:
        return AgentName.MINI_SWE_AGENT_DEEPMORPH.value

    async def install(self, environment: BaseEnvironment) -> None:
        await environment.upload_dir(self._local_package_path, _CONTAINER_PKG_PATH)

        for step in self.install_spec().steps:
            run = step.run.replace(
                f"uv tool install {self._AGENT_PACKAGE}",
                f"uv tool install {_CONTAINER_PKG_PATH}",
            )
            if step.user == "root":
                await self.exec_as_root(environment, command=run, env=step.env)
            else:
                await self.exec_as_agent(environment, command=run, env=step.env)
