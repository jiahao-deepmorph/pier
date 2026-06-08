from pathlib import Path
from typing import ClassVar

from pier.agents.installed.mini_swe_agent import MiniSweAgent
from pier.environments.base import BaseEnvironment
from pier.models.agent.install import AgentInstallSpec
from pier.models.agent.name import AgentName


_CONTAINER_PKG_PATH = "/tmp/mini-swe-agent-deepmorph-src"
_DEFAULT_LOCAL_PATH = Path(__file__).parents[4] / "mini-swe-agent-deepmorph"


class MiniSweAgentDeepmorphh(MiniSweAgent):
    """
    Variant of MiniSweAgent that installs mini-swe-agent-deepmorph from a local source tree.

    For Docker builds the source tree is COPYed into the build context.
    For runtime installs (modal, daytona) it is uploaded via upload_dir.
    """

    _AGENT_PACKAGE: ClassVar[str] = "mini-swe-agent-deepmorph"
    _AGENT_EXECUTABLE: ClassVar[str] = "mini-swe-agent-deepmorph"

    def __init__(self, *args, local_package_path: Path | str = _DEFAULT_LOCAL_PATH, **kwargs):
        super().__init__(*args, **kwargs)
        self._local_package_path = Path(local_package_path)

    @staticmethod
    def name() -> str:
        return AgentName.MINI_SWE_AGENT_DEEPMORPH.value

    def install_spec(self) -> AgentInstallSpec:
        spec = super().install_spec()
        new_steps = [
            step.model_copy(update={
                "run": step.run.replace(
                    f"uv tool install {self._AGENT_PACKAGE}",
                    f"uv tool install {_CONTAINER_PKG_PATH}",
                )
            })
            for step in spec.steps
        ]
        return spec.model_copy(update={
            "steps": new_steps,
            "build_context_dirs": [(str(self._local_package_path), _CONTAINER_PKG_PATH)],
        })

    async def install(self, environment: BaseEnvironment) -> None:
        await environment.upload_dir(self._local_package_path, _CONTAINER_PKG_PATH)
        await super().install(environment)
