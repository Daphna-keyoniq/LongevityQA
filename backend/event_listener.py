from datetime import datetime
from typing import Optional

from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
)
from crewai.utilities.events.base_event_listener import BaseEventListener
from config import Config

## Internal imports
from utils.task_manager import TaskManagerRepository, TaskStatus

config = Config.load_configuration()

class EventListener(BaseEventListener):
    def __init__(self, task_manager: TaskManagerRepository = None, task_id: Optional[str] = None):
        super().__init__()
        self.task_manager = task_manager
        self.task_id = task_id

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            if self.task_id:
                self.task_manager.save_task(
                    task_status=TaskStatus(
                        task_id=self.task_id,
                        status="processing",
                        message=f"Crew {event.crew_name} has started execution!",
                        record_entered_timestamp=datetime.now()
                    )
                )

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            if self.task_id:
                self.task_manager.save_task(
                    task_status=TaskStatus(
                        task_id=self.task_id,
                        status="processing",
                        message=f"Crew {event.crew_name} has completed execution!",
                        record_entered_timestamp=datetime.now()
                    )
                )
        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Agent {event.agent.role} completed task!")
