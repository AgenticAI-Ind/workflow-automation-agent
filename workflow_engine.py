"""
Workflow Execution Engine
Orchestrates multi-step workflows with conditional logic
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import asyncio


class WorkflowEngine:
    """Core workflow execution engine"""

    def __init__(self):
        self.workflows = {}
        self.executions = {}

    async def create_workflow(
        self,
        name: str,
        trigger: Dict,
        actions: List[Dict],
        conditions: Optional[Dict] = None
    ) -> Dict:
        """
        Create a new workflow

        Args:
            name: Workflow name
            trigger: Trigger configuration
            actions: List of actions to execute
            conditions: Conditional logic

        Returns:
            Created workflow details
        """
        workflow_id = f"wf_{len(self.workflows) + 1}"

        workflow = {
            "id": workflow_id,
            "name": name,
            "trigger": trigger,
            "actions": actions,
            "conditions": conditions or {},
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }

        self.workflows[workflow_id] = workflow
        return workflow

    async def execute_workflow(
        self,
        workflow_id: str,
        input_data: Optional[Dict] = None
    ) -> Dict:
        """
        Execute a workflow

        Args:
            workflow_id: Workflow to execute
            input_data: Input data for workflow

        Returns:
            Execution results
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        execution_id = f"exec_{len(self.executions) + 1}"
        start_time = datetime.now()

        results = []

        # Execute each action
        for i, action in enumerate(workflow["actions"]):
            try:
                result = await self._execute_action(action, input_data)
                results.append({
                    "action": action["action"],
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "action": action["action"],
                    "status": "failed",
                    "error": str(e)
                })
                break

        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        execution = {
            "id": execution_id,
            "workflow_id": workflow_id,
            "started_at": start_time.isoformat(),
            "completed_at": end_time.isoformat(),
            "duration_ms": duration_ms,
            "status": "completed",
            "results": results
        }

        self.executions[execution_id] = execution
        return execution

    async def _execute_action(
        self,
        action: Dict,
        input_data: Optional[Dict]
    ) -> Any:
        """Execute a single action"""
        app = action.get("app")
        action_type = action.get("action")

        # Simulate action execution
        await asyncio.sleep(0.1)

        return {
            "app": app,
            "action": action_type,
            "executed": True
        }

    def list_workflows(self) -> List[Dict]:
        """List all workflows"""
        return list(self.workflows.values())

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow details"""
        return self.workflows.get(workflow_id)
